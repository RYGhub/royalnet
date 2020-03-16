from typing import *
from ..tables import DndBattleUnit
from .abstract import DndBattleTargetCommand


class DndextraCommand(DndBattleTargetCommand):
    name: str = "dndextra"

    description: str = "Change the extras for a target in the current battle."

    syntax: str = "{target} {extra}"

    aliases = ["extra", "dextra"]

    async def _change(self, unit: DndBattleUnit, args: List[str]):
        unit.extra = " ".join(args)
