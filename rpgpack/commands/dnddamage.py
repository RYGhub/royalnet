from typing import *
from ..tables import DndBattleUnit
from .abstract import DndBattleTargetCommand


class DnddamageCommand(DndBattleTargetCommand):
    name: str = "dnddamage"

    description: str = "Damage a target in the currently active battle."

    syntax: str = "{target} {damage}"

    aliases = ["damage", "ddamage", "dd"]

    async def _change(self, unit: DndBattleUnit, args: List[str]):
        health = unit.health
        health.change(-int(args[0]))
        unit.health = health
