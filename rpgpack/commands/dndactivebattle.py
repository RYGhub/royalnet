from royalnet.commands import *
from royalnet.utils import asyncify
from ..tables import DndCharacter, DndActiveBattle, DndBattle
from ..utils import get_active_battle, get_interface_data
import pickle


class DndactivebattleCommand(Command):
    name: str = "dndactivebattle"

    description: str = "Set a D&D battle as active."

    aliases = ["dab", "dndab", "activebattle", "dactivebattle"]

    syntax = "{name|id}"

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        BattleT = self.alchemy.get(DndBattle)
        ABattleT = self.alchemy.get(DndActiveBattle)

        identifier = args.joined()
        active_battle = await get_active_battle(data)

        # Display the active character
        if identifier == "":
            if active_battle is None:
                await data.reply("ℹ️ No battles have ever been activated in this chat.")
            else:
                await data.reply(active_battle.battle.create_message())
            return

        # Find the battle
        try:
            identifier = int(identifier)
        except ValueError:
            # Find the battle by name
            battles = await asyncify(data.session.query(BattleT).filter_by(name=identifier).all)
            if len(battles) >= 2:
                char_string = "\n".join([f"[c]{battle.id}[/c]" for battle in battles])
                raise CommandError(f"Multiple battles share the name [b]{identifier}[/b], "
                                   f"please activate one of them by using their id:\n{char_string}")
            elif len(battles) == 1:
                battle = battles[0]
            else:
                battle = None
        else:
            # Find the battle by id
            battle = await asyncify(data.session.query(BattleT)
                                        .filter_by(id=identifier)
                                        .one_or_none)
        if battle is None:
            raise CommandError("No such battle found.")
        # Check if the player already has an active character
        if active_battle is None:
            # Create a new active battle
            active_battle = ABattleT(
                battle=battle,
                interface_name=self.interface.name,
                interface_data=pickle.dumps(get_interface_data(data)))
            data.session.add(active_battle)
        else:
            # Change the active character
            active_battle.battle = battle
        await data.session_commit()
        await data.reply(f"⚔️ [b]{battle}[/b]! Roll initiative!")
