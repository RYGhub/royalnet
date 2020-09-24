from typing import *
import royalnet.commands as rc
import royalnet.utils as ru
import royalnet.serf.telegram as rst
import royalnet.backpack.tables as rbt
import abc
import logging
import asyncio as aio
from ...types import Updatable


log = logging.getLogger(__name__)


class LinkerCommand(rc.Command, metaclass=abc.ABCMeta):

    def __init__(self, serf, config):
        super().__init__(serf, config)
        self.updater_task = None
        if self.enabled():
            self.updater_task = self.loop.create_task(self.run_updater())

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        async with data.session_acm() as session:
            author = await data.find_author(session=session, required=True)
            if len(args) == 0:
                message = []
                for obj in await self.get_updatables_of_user(session=session, user=author):
                    async def change(attribute: str, value: Any):
                        """A shortcut for self.__change."""
                        await self._change(session=session,
                                           obj=obj,
                                           attribute=attribute,
                                           new=value)

                    await self.update(session=session, obj=obj, change=change)
                    message.append(self.describe(obj))
                if len(message) == 0:
                    raise rc.UserError("Nessun account connesso.")
                await ru.asyncify(session.commit)
                await data.reply("\n".join(message))
            else:
                created = await self.create(session=session, user=author, args=args, data=data)
                await ru.asyncify(session.commit)
                if created is not None:
                    message = ["🔗 Account collegato!", "", self.describe(created)]
                    await data.reply("\n".join(message))

    def describe(self, obj: Updatable) -> str:
        """The text that should be appended to the report message for a given Updatable."""
        return str(obj)

    @abc.abstractmethod
    async def get_updatables_of_user(self, session, user: rbt.User) -> List[Updatable]:
        """Get the updatables of a specific user."""
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_updatables(self, session) -> List[Updatable]:
        """Return a list of all objects that should be updated at this updater cycle."""
        raise NotImplementedError()

    @abc.abstractmethod
    async def create(self,
                     session,
                     user: rbt.User,
                     args: rc.CommandArgs,
                     data: Optional[rc.CommandData] = None) -> Optional[Updatable]:
        """Create a new updatable object for a user.

        This function is responsible for adding the object to the session."""
        raise NotImplementedError()

    @abc.abstractmethod
    async def update(self, session, obj, change: Callable[[str, Any], Awaitable[None]]):
        """Update a single updatable object. Use the change method to change values on the object!"""
        raise NotImplementedError()

    @abc.abstractmethod
    async def on_increase(self, session, obj: Updatable, attribute: str, old: Any, new: Any) -> None:
        """Called when the attribute has increased from the old value."""
        raise NotImplementedError()

    @abc.abstractmethod
    async def on_unchanged(self, session, obj: Updatable, attribute: str, old: Any, new: Any) -> None:
        """Called when the attribute stayed the same as the old value."""
        raise NotImplementedError()

    @abc.abstractmethod
    async def on_decrease(self, session, obj: Updatable, attribute: str, old: Any, new: Any) -> None:
        """Called when the attribute has decreased from the old value."""
        raise NotImplementedError()

    @abc.abstractmethod
    async def on_first(self, session, obj: Updatable, attribute: str, old: None, new: Any) -> None:
        """Called when the attribute changed from None."""
        raise NotImplementedError()

    @abc.abstractmethod
    async def on_reset(self, session, obj: Updatable, attribute: str, old: Any, new: None) -> None:
        """Called when the attribute changed to None."""
        raise NotImplementedError()

    async def _change(self,
                      session,
                      obj,
                      attribute: str,
                      new) -> None:
        """Set the value of an attribute of an object to a value, and call the corresponding method."""
        old = obj.__getattribute__(attribute)
        if new == old:
            await self.on_unchanged(session=session,
                                    obj=obj,
                                    attribute=attribute,
                                    old=old,
                                    new=new)
        else:
            if old is None:
                await self.on_first(session=session,
                                    obj=obj,
                                    attribute=attribute,
                                    old=old,
                                    new=new)
            elif new is None:
                await self.on_reset(session=session,
                                    obj=obj,
                                    attribute=attribute,
                                    old=old,
                                    new=new)
            elif new > old:
                await self.on_increase(session=session,
                                       obj=obj,
                                       attribute=attribute,
                                       old=old,
                                       new=new)
            else:
                await self.on_decrease(session=session,
                                       obj=obj,
                                       attribute=attribute,
                                       old=old,
                                       new=new)
        obj.__setattr__(attribute, new)

    def enabled(self) -> bool:
        """Whether the updater is enabled or not."""
        return self.config[self.name]["updater"]["enabled"] and isinstance(self.serf, rst.TelegramSerf)

    def period(self) -> int:
        """The time between two updater cycles."""
        return self.config[self.name]["updater"]["period"]

    def delay(self) -> int:
        """The time between two object updates."""
        return self.config[self.name]["updater"]["delay"]

    def target(self) -> int:
        """The id of the Telegram chat where notifications should be sent."""
        return self.config[self.name]["updater"]["target"]

    async def run_updater(self):
        log.info(f"Starting updater: {self.name}")

        while True:
            log.debug(f"Updater cycle: {self.name}")
            session = self.alchemy.Session()
            objects = await self.get_updatables(session)

            for index, obj in enumerate(objects):
                log.debug(f"Updating: {obj} ({self.name})")

                async def change(attribute: str, value: Any):
                    """A shortcut for self.__change."""
                    await self._change(session=session,
                                       obj=obj,
                                       attribute=attribute,
                                       new=value)

                try:
                    await self.update(session=session,
                                      obj=obj,
                                      change=change)
                except Exception as e:
                    ru.sentry_exc(e)

                if index < len(objects) - 1:
                    delay = self.delay()
                    log.debug(f"Waiting for: {delay} seconds (delay)")
                    await aio.sleep(delay)

            log.debug(f"Committing updates: {self.name}")
            await ru.asyncify(session.commit)
            session.close()

            period = self.period()
            log.debug(f"Waiting for: {period} seconds (period)")
            await aio.sleep(period)

    async def notify(self, message):
        await self.serf.api_call(self.serf.client.send_message,
                                 chat_id=self.target(),
                                 text=rst.escape(message),
                                 parse_mode="HTML",
                                 disable_webpage_preview=True)
