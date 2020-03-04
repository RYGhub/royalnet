from typing import *
import royalnet
import royalnet.commands as rc
import royalnet.utils as ru
from ..types import Faction, Health
from ..tables import DndBattleUnit
from ..utils import get_active_battle


class DndaddunitCommand(rc.Command):
    name: str = "dndaddunit"

    description: str = "Add an Unit to a Battle."

    aliases = ["dau", "dndau", "daddunit", ""]

    syntax: str = "{faction} {name} {initiative} {health} {armorclass}"

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        faction = Faction[args[0].upper()]
        name = args[1]
        initiative = int(args[2])
        health = args[3]
        armor_class = int(args[4])

        DndBattleUnitT = self.alchemy.get(DndBattleUnit)

        active_battle = await get_active_battle(data)
        if active_battle is None:
            raise rc.CommandError("No battle is active in this chat.")

        dbu = DndBattleUnitT(
            initiative=initiative,
            faction=faction,
            name=name,
            health_string=health,
            armor_class=armor_class,
            battle=active_battle.battle
        )

        data.session.add(dbu)
        await data.session_commit()

        await data.reply(f"✅ [b]{dbu.name}[/b] joined the battle!\n"
                         f"{dbu}")
