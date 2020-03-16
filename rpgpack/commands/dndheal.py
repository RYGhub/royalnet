from typing import *
from ..tables import DndBattleUnit
from .abstract import DndBattleTargetCommand


class DndhealCommand(DndBattleTargetCommand):
    name: str = "dndheal"

    description: str = "Heal a target in the currently active battle."

    syntax: str = "{target} {heal}"

    aliases = ["heal", "dheal"]

    async def _change(self, unit: DndBattleUnit, args: List[str]):
        health = unit.health
        health.change(int(args[0]))
        unit.health = health
