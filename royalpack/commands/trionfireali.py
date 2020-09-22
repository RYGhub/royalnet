from typing import *
import logging
import aiohttp
import royalnet.commands as rc
import royalnet.utils as ru
from royalnet.backpack import tables as rbt
from .abstract.linker import LinkerCommand

from ..tables import Steam, Dota
from ..types import DotaRank

log = logging.getLogger(__name__)


class TrionfirealiCommand(LinkerCommand):
    name: str = "trionfireali"

    description: str = "Visualizza il tuo pr⊕gress⊕ nei Tri⊕nfi Reali!"

    syntax: str = ""

    def describe(self, obj: Steam) -> str:
        raise NotImplementedError()

    async def get_updatables_of_user(self, session, user: rbt.User) -> List[Dota]:
        raise NotImplementedError()

    async def get_updatables(self, session) -> List[Dota]:
        raise NotImplementedError()

    async def create(self,
                     session,
                     user: rbt.User,
                     args: rc.CommandArgs,
                     data: Optional[rc.CommandData] = None) -> Optional[Dota]:
        raise rc.InvalidInputError("Trionfi Reali accounts are automatically linked from Steam.")

    async def update(self, session, obj: Steam, change: Callable[[str, Any], Awaitable[None]]):
        raise NotImplementedError()

    async def on_increase(self, session, obj: Dota, attribute: str, old: Any, new: Any) -> None:
        pass

    async def on_unchanged(self, session, obj: Dota, attribute: str, old: Any, new: Any) -> None:
        pass

    async def on_decrease(self, session, obj: Dota, attribute: str, old: Any, new: Any) -> None:
        pass

    async def on_first(self, session, obj: Dota, attribute: str, old: None, new: Any) -> None:
        pass

    async def on_reset(self, session, obj: Dota, attribute: str, old: Any, new: None) -> None:
        pass
