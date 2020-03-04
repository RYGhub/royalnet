from typing import *
import royalnet.commands as rc
import royalnet.utils as ru

from ..tables import DndBattleUnit
from .getactivebattle import get_active_battle
from .getactivechar import get_active_character

from sqlalchemy import func, and_


async def find_unit_in_current_battle(data: rc.CommandData, name: Optional[str]) -> Optional[DndBattleUnit]:
    DndBattleUnitT = data._interface.alchemy.get(DndBattleUnit)

    active_battle = await get_active_battle(data)
    if active_battle is None:
        raise rc.CommandError("No battle is active in this chat.")

    if name is None:
        active_character = await get_active_character(data)
        if active_character is None:
            raise rc.InvalidInputError("You currently have no active character.")

        unit = await ru.asyncify(data.session.query(DndBattleUnitT).filter_by(
            linked_character=active_character.character,
            battle=active_battle.battle
        ).one_or_none)
        if unit is None:
            raise rc.InvalidInputError("Your active character is not fighting in this battle.")

    else:
        unit = await ru.asyncify(data.session.query(DndBattleUnitT).filter(and_(
            func.lower(DndBattleUnitT.name) == func.lower(name),
            DndBattleUnitT.battle == active_battle.battle
        )).one_or_none)
        if unit is None:
            return None

    return unit
