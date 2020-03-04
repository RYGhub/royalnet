from typing import *
import royalnet
import royalnet.commands as rc
import royalnet.utils as ru
from ..tables import DndBattleUnit
from ..utils import find_unit_in_current_battle


class DndextraCommand(rc.Command):
    name: str = "dndextra"

    description: str = "Change the extras for a unit in the current battle."

    syntax: str = "[name] {extra}"

    aliases = ["extra", "dextra"]

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        name = args.optional(0)
        extra = " ".join(args[1:])

        if name is not None:
            unit: Optional[DndBattleUnit] = await find_unit_in_current_battle(data, name)
        else:
            unit = None

        if unit is None:
            extra = " ".join(args)
            unit: Optional[DndBattleUnit] = await find_unit_in_current_battle(data, None)

        unit.extra = extra
        await data.session_commit()
        await data.reply(f"{unit}")
