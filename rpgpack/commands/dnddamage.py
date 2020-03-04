from typing import *
import royalnet
import royalnet.commands as rc
import royalnet.utils as ru
from ..tables import DndBattleUnit
from ..utils import find_unit_in_current_battle


class DnddamageCommand(rc.Command):
    name: str = "dnddamage"

    description: str = "Damage a unit in the currently active battle."

    syntax: str = "[name] {damage}"

    aliases = ["dmg", "ddmg", "dnddmg", "damage", "ddamage"]

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        if len(args) > 1:
            name = args[0]
            damage = int(args[1])
        else:
            name = None
            damage = int(args[0])

        unit = await find_unit_in_current_battle(data, name)
        if unit is None:
            raise rc.InvalidInputError("No such unit is fighting in the currently active battle.")

        health = unit.health
        health.change(-damage)
        unit.health = health
        await data.session_commit()
        await data.reply(f"{unit}")
