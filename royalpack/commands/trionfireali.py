from typing import *
import logging
import royalnet.commands as rc
import royalnet.utils as ru
from royalnet.backpack import tables as rbt
from .abstract.linker import LinkerCommand
import asyncio
import datetime

from ..halloween2020 import *

log = logging.getLogger(__name__)


class TrionfirealiCommand(LinkerCommand):
    name: str = "trionfireali"

    description: str = "Visualizza il tuo pr⊕gress⊕ nei Tri⊕nfi Reali!"

    syntax: str = ""

    def describe(self, obj: TrionfiStatus) -> str:
        raise NotImplementedError()

    async def get_updatables_of_user(self, session, user: rbt.User) -> List[TrionfiStatus]:
        return [user.halloween2020] if user.halloween2020 else []

    async def get_updatables(self, session) -> List[TrionfiStatus]:
        return await ru.asyncify(session.query(self.alchemy.get(TrionfiStatus)).all)

    async def create(self,
                     session,
                     user: rbt.User,
                     args: rc.CommandArgs,
                     data: Optional[rc.CommandData] = None) -> Optional[TrionfiStatus]:
        raise rc.InvalidInputError("N⊕n è qui che inizia il mister⊕.")

    async def update(self, session, obj: TrionfiStatus, change: Callable[[str, Any], Awaitable[None]]):
        for trionfo in trionfilist:
            check_result = await trionfo.check.check(obj, key=self.config["steampowered"]["token"])
            log.debug(f"{trionfo.check}: {check_result}")
            if check_result is True:
                obj.__setattr__(trionfo.variable, datetime.datetime.now())
            await asyncio.sleep(1)

    async def on_increase(self, session, obj: TrionfiStatus, attribute: str, old: Any, new: Any) -> None:
        pass

    async def on_unchanged(self, session, obj: TrionfiStatus, attribute: str, old: Any, new: Any) -> None:
        pass

    async def on_decrease(self, session, obj: TrionfiStatus, attribute: str, old: Any, new: Any) -> None:
        pass

    async def on_first(self, session, obj: TrionfiStatus, attribute: str, old: None, new: Any) -> None:
        pass

    async def on_reset(self, session, obj: TrionfiStatus, attribute: str, old: Any, new: None) -> None:
        pass
