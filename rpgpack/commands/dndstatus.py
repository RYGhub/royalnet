from typing import *
import royalnet
import royalnet.commands as rc
import royalnet.utils as ru
from ..tables import DndBattleUnit
from ..utils import find_unit_in_current_battle


class DndstatusCommand(rc.Command):
    name: str = "dndstatus"

    description: str = "Change the status for a unit in the current battle."

    syntax: str = "[name] {status}"

    aliases = ["status", "dstatus"]

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        name = args.optional(0)
        status = " ".join(args[1:])

        if name is not None:
            unit: Optional[DndBattleUnit] = await find_unit_in_current_battle(data, name)
        else:
            unit = None

        if unit is None:
            status = " ".join(args)
            unit: Optional[DndBattleUnit] = await find_unit_in_current_battle(data, None)


        unit.status = status
        await data.session_commit()
        await data.reply(f"{unit}")
