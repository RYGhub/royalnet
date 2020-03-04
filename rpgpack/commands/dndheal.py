from typing import *
import royalnet
import royalnet.commands as rc
import royalnet.utils as ru
from ..tables import DndBattleUnit
from ..utils import find_unit_in_current_battle


class DndhealCommand(rc.Command):
    name: str = "dndheal"

    description: str = "Heal a unit in the currently active battle."

    syntax: str = "[name] {heal}"

    aliases = ["heal", "dheal"]

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        if len(args) > 1:
            name = args[0]
            heal = int(args[1])
        else:
            name = None
            heal = int(args[0])

        unit = await find_unit_in_current_battle(data, name)
        if unit is None:
            raise rc.InvalidInputError("No such unit is fighting in the currently active battle.")

        health = unit.health
        health.change(heal)
        unit.health = health
        await data.session_commit()
        await data.reply(f"{unit}")
