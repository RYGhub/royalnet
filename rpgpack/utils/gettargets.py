from typing import *
import royalnet.commands as rc
import royalnet.utils as ru
from ..tables import DndBattleUnit
from .getactivebattle import get_active_battle
from .getactivechar import get_active_character
from ..types.faction import Faction
from sqlalchemy import and_


async def get_targets(data: rc.CommandData, target: Optional[str]) -> List[DndBattleUnit]:
    DndBattleUnitT = data._interface.alchemy.get(DndBattleUnit)

    active_battle = await get_active_battle(data)
    if active_battle is None:
        raise rc.CommandError("No battle is active in this chat.")
    battle = active_battle.battle

    # Get the active character
    if not target or target.upper() == "SELF":
        active_character = await get_active_character(data)
        if active_character is None:
            return []
        char = active_character.character

        return await ru.asyncify(data.session.query(DndBattleUnitT).filter_by(
            linked_character=char,
            battle=battle
        ).all)

    # Get all
    if target.upper() == "ALL":
        return await ru.asyncify(data.session.query(DndBattleUnitT).filter_by(
            battle=battle
        ).all)

    # Get by faction
    try:
        faction = Faction.get(target)
    except ValueError:
        pass
    else:
        return await ru.asyncify(data.session.query(DndBattleUnitT).filter_by(
            faction=faction,
            battle=battle
        ).all)

    # Get by ilike
    return await ru.asyncify(data.session.query(DndBattleUnitT).filter(and_(
        DndBattleUnitT.name.ilike(target),
        DndBattleUnitT.battle == battle
    )).all)
