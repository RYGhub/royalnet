from typing import *

import asyncio
import logging
import aiohttp

from royalnet.backpack import tables as rbt
import royalnet.commands as rc
import royalnet.utils as ru
from sqlalchemy import or_, and_

from .abstract.linker import LinkerCommand
from ..tables import Steam, Brawlhalla, BrawlhallaDuo
from ..types import BrawlhallaRank, BrawlhallaMetal, BrawlhallaTier, Updatable

log = logging.getLogger(__name__)


class BrawlhallaCommand(LinkerCommand):
    name: str = "brawlhalla"

    aliases = ["bh", "bruhalla", "bruhlalla"]

    description: str = "Visualizza le tue statistiche di Brawlhalla."

    syntax: str = ""

    def token(self):
        return self.config['brawlhalla']['token']

    async def get_updatables_of_user(self, session, user: rbt.User) -> List[Brawlhalla]:
        return user.steam

    async def get_updatables(self, session) -> List[Brawlhalla]:
        return await ru.asyncify(session.query(self.alchemy.get(Steam)).all)

    async def create(self,
                     session,
                     user: rbt.User,
                     args: rc.CommandArgs,
                     data: Optional[rc.CommandData] = None) -> Optional[Brawlhalla]:
        raise rc.InvalidInputError("Brawlhalla accounts are automatically linked from Steam.")

    async def update(self, session, obj, change: Callable[[str, Any], Awaitable[None]]):
        BrawlhallaT = self.alchemy.get(Brawlhalla)
        DuoT = self.alchemy.get(BrawlhallaDuo)
        log.info(f"Updating: {obj}")
        async with aiohttp.ClientSession() as hcs:
            bh: Brawlhalla = obj.brawlhalla
            if bh is None:
                log.debug(f"Checking if player has an account...")
                async with hcs.get(f"https://api.brawlhalla.com/search?steamid={obj.steamid.as_64}&api_key={self.token()}") as response:
                    if response.status != 200:
                        raise rc.ExternalError(f"Brawlhalla API /search returned {response.status}!")
                    j = await response.json()
                    if j == {} or j == []:
                        log.debug("No account found.")
                        return
                    bh = BrawlhallaT(
                        steam=obj,
                        brawlhalla_id=j["brawlhalla_id"],
                        name=j["name"]
                    )
                    session.add(bh)
                    session.flush()

            async with hcs.get(f"https://api.brawlhalla.com/player/{bh.brawlhalla_id}/ranked?api_key={self.token()}") as response:
                if response.status != 200:
                    raise rc.ExternalError(f"Brawlhalla API /ranked returned {response.status}!")
                j = await response.json()
                if j == {} or j == []:
                    log.debug("No ranked info found.")
                else:
                    await self._change(session=session, obj=bh, attribute="rating_1v1", new=j["rating"])
                    metal_name, tier_name = j["tier"].split(" ", 1)
                    metal = BrawlhallaMetal[metal_name.upper()]
                    tier = BrawlhallaTier(int(tier_name))
                    rank = BrawlhallaRank(metal=metal, tier=tier)
                    await self._change(session=session, obj=bh, attribute="rank_1v1", new=rank)

                    for jduo in j.get("2v2", []):
                        bhduo: Optional[BrawlhallaDuo] = await ru.asyncify(
                            session.query(DuoT)
                                .filter(
                                    or_(
                                        and_(
                                            DuoT.id_one == jduo["brawlhalla_id_one"],
                                            DuoT.id_two == jduo["brawlhalla_id_two"]
                                        ),
                                        and_(
                                            DuoT.id_one == jduo["brawlhalla_id_two"],
                                            DuoT.id_two == jduo["brawlhalla_id_one"]
                                        )
                                    )
                                )
                                .one_or_none
                        )
                        if bhduo is None:
                            if bh.brawlhalla_id == jduo["brawlhalla_id_one"]:
                                otherbh: Optional[Brawlhalla] = await ru.asyncify(
                                    session.query(BrawlhallaT).get, jduo["brawlhalla_id_two"]
                                )
                            else:
                                otherbh: Optional[Brawlhalla] = await ru.asyncify(
                                    session.query(BrawlhallaT).get, jduo["brawlhalla_id_one"]
                                )
                            if otherbh is None:
                                continue
                            bhduo = DuoT(
                                one=bh,
                                two=otherbh,
                            )

                            session.add(bhduo)
                        await self._change(session=session, obj=bhduo, attribute="rating_2v2", new=jduo["rating"])
                        metal_name, tier_name = jduo["tier"].split(" ", 1)
                        metal = BrawlhallaMetal[metal_name.upper()]
                        tier = BrawlhallaTier(int(tier_name))
                        rank = BrawlhallaRank(metal=metal, tier=tier)
                        await self._change(session=session, obj=bhduo, attribute="rank_2v2", new=rank)

    async def on_increase(self, session, obj: Union[Brawlhalla, BrawlhallaDuo], attribute: str, old: Any, new: Any) -> None:
        if attribute == "rank_1v1":
            await self.notify(f"📈 [b]{obj.steam.user}[/b] è salito a [b]{new}[/b] ({obj.rating_1v1} MMR) in 1v1 su Brawlhalla! Congratulazioni!")
        elif attribute == "rank_2v2":
            await self.notify(f"📈 [b]{obj.one.steam.user}[/b] e [b]{obj.two.steam.user}[/b] sono saliti a [b]{new}[/b] ({obj.rating_2v2} MMR) in 2v2 su Brawlhalla! Congratulazioni!")

    async def on_unchanged(self, session, obj: Union[Brawlhalla, BrawlhallaDuo], attribute: str, old: Any, new: Any) -> None:
        pass

    async def on_decrease(self, session, obj: Union[Brawlhalla, BrawlhallaDuo], attribute: str, old: Any, new: Any) -> None:
        if attribute == "rank_1v1":
            await self.notify(f"📉 [b]{obj.steam.user}[/b] è sceso a [b]{new}[/b] ({obj.rating_1v1} MMR) in 1v1 su Brawlhalla.")
        elif attribute == "rank_2v2":
            await self.notify(f"📉 [b]{obj.one.steam.user}[/b] e [b]{obj.two.steam.user}[/b] sono scesi a [b]{new}[/b] ({obj.rating_2v2} MMR) in 2v2 su Brawlhalla.")

    async def on_first(self, session, obj: Union[Brawlhalla, BrawlhallaDuo], attribute: str, old: None, new: Any) -> None:
        if attribute == "rank_1v1":
            await self.notify(f"🌟 [b]{obj.steam.user}[/b] si è classificato a [b]{new}[/b] ({obj.rating_1v1} MMR) in 1v1 su Brawlhalla!")
        elif attribute == "rank_2v2":
            await self.notify(f"🌟 [b]{obj.one.steam.user}[/b] e [b]{obj.two.steam.user}[/b] si sono classificati a [b]{new}[/b] ({obj.rating_2v2} MMR) in 2v2 su Brawlhalla!")

    async def on_reset(self, session, obj: Union[Brawlhalla, BrawlhallaDuo], attribute: str, old: Any, new: None) -> None:
        if attribute == "rank_1v1":
            await self.notify(f"⬜️ [b]{obj.steam.user}[/b] non ha più un rank su Brawlhalla.")
        elif attribute == "rank_2v2":
            await self.notify(f"⬜️ [b]{obj.one.steam.user}[/b] e [b]{obj.two.steam.user}[/b] non hanno più un rank su Brawlhalla.")

    def describe(self, obj: Steam) -> str:
        bh = obj.brawlhalla

        string = [f"ℹ️ [b]{bh.name}[/b]", ""]

        if bh.rank_1v1:
            string.append("👤 [b]1v1[/b]")
            string.append(f"[b]{bh.rank_1v1}[/b] ({bh.rating_1v1} MMR)")
            string.append("")

        if len(bh.duos) != 0:
            string.append(f"👥 [b]2v2[/b]")

        for duo in sorted(bh.duos, key=lambda d: -d.rating_2v2):
            other = duo.other(bh)
            string.append(f"Con [b]{other.steam.user}[/b]: [b]{duo.rank_2v2}[/b] ({duo.rating_2v2} MMR)")

        if len(bh.duos) != 0:
            string.append("")

        return "\n".join(string)
