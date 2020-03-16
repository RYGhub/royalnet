from typing import *
from ..tables import DndBattleUnit
from .abstract import DndBattleTargetCommand


class DndstatusCommand(DndBattleTargetCommand):
    name: str = "dndstatus"

    description: str = "Change the target for a unit in the current battle."

    syntax: str = "{target} {status}"

    aliases = ["status", "dstatus"]

    async def _change(self, unit: DndBattleUnit, args: List[str]):
        unit.status = " ".join(args)
