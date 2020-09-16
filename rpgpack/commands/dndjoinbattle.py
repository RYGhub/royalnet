from typing import *
import random
import royalnet
import royalnet.commands as rc
import royalnet.utils as ru
from ..types import Faction
from ..tables import DndBattleUnit, DndCharacter
from ..utils import get_active_battle, get_active_character


class DndjoinbattleCommand(rc.Command):
    name: str = "dndjoinbattle"

    description: str = "Add your currently active character to the currently active battle."

    aliases = ["joinbattle", "djoinbattle"]

    syntax: str = "{faction} {initiative_mod}"

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        faction = Faction[args[0].upper()]
        initiative_mod = int(args.optional(1, default="0"))

        async with data.session_acm() as session:
            DndBattleUnitT = self.alchemy.get(DndBattleUnit)

            active_battle = await get_active_battle(data=data, session=session)
            if active_battle is None:
                raise rc.CommandError("No battle is active in this chat.")

            active_character = await get_active_character(data=data, session=session)
            if active_character is None:
                raise rc.CommandError("You don't have an active character.")

            char: DndCharacter = active_character.character

            units_with_same_name = await ru.asyncify(session.query(DndBattleUnitT).filter_by(
                name=char.name,
                battle=active_battle.battle
            ).all)

            if len(units_with_same_name) != 0:
                raise rc.InvalidInputError("A unit with the same name already exists.")

            roll = random.randrange(1, 21)
            modifier = char.initiative + initiative_mod
            modifier_str = f"{modifier:+d}" if modifier != 0 else ""
            initiative = roll + modifier

            dbu = DndBattleUnitT(
                linked_character=char,
                initiative=initiative,
                faction=faction,
                name=char.name,
                health_string=f"{char.current_hp}/{char.max_hp}",
                armor_class=char.armor_class,
                battle=active_battle.battle
            )

            session.add(dbu)
            await ru.asyncify(session.commit)

            await data.reply(f"{dbu}\n"
                             f"joins the battle!\n"
                             f"\n"
                             f"🎲 1d20{modifier_str} = {roll}{modifier_str} = {initiative}")
