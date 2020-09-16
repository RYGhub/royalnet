import abc
from typing import *
import royalnet
import royalnet.commands as rc
import royalnet.utils as ru
from ...tables import DndBattleUnit
from ...utils import get_targets


class DndBattleTargetCommand(rc.Command, abc.ABC):
    @abc.abstractmethod
    async def _change(self, unit: DndBattleUnit, args: List[str]):
        raise NotImplementedError()

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        target = args[0]

        async with data.session_acm() as session:
            units = await get_targets(target, data=data, session=session)
            if len(units) == 0:
                raise rc.InvalidInputError(f"No targets found matching [c]{target}[/c].")

            for unit in units:
                await self._change(unit, args[1:])

            await session.commit()

            message = []
            for unit in units:
                message.append(f"{unit}")

            await data.reply("\n\n".join(message))
