from typing import *
import royalnet
import royalnet.commands as rc
import royalnet.utils as ru
from ..tables import DndBattleUnit
from ..utils import find_unit_in_current_battle


class DnddeathsaveCommand(rc.Command):
    name: str = "dnddeathsave"

    description: str = "Add a death save result to a unit in the currently active battle."

    syntax: str = "[name] {s|f}"

    aliases = ["deathsave", "ddeathsave", "ds", "dds", "dndds"]

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        if len(args) > 1:
            name = args[0]
            result = args[1].lower()
        else:
            name = None
            result = args[0].lower()

        unit = await find_unit_in_current_battle(data, name)
        if unit is None:
            raise rc.InvalidInputError("No such unit is fighting in the currently active battle.")

        health = unit.health
        if result[0] == "s":
            health.deathsave_success()
        elif result[0] == "f":
            health.deathsave_failure()
        else:
            raise rc.InvalidInputError("Unknown result type")
        unit.health = health

        await data.session_commit()
        await data.reply(f"{unit}")
