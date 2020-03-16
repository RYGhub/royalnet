from typing import *
import royalnet.commands as rc
from ..tables import DndBattleUnit
from .abstract import DndBattleTargetCommand


class DnddeathsaveCommand(DndBattleTargetCommand):
    name: str = "dnddeathsave"

    description: str = "Add a death save result to a target in the currently active battle."

    syntax: str = "{target} {s|f}"

    aliases = ["deathsave", "ddeathsave", "ds", "dds", "dndds"]

    async def _change(self, unit: DndBattleUnit, args: List[str]):
        health = unit.health
        if args[0][0] == "s":
            health.deathsave_success()
        elif args[0][0] == "f":
            health.deathsave_failure()
        else:
            raise rc.InvalidInputError(f"Unknown result type [c]{args[0][0]}[/c].")
        unit.health = health
