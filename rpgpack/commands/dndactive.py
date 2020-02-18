from royalnet.commands import *
from royalnet.utils import asyncify
from ..tables import DndCharacter, DndActiveCharacter
from ..utils import get_active_character, get_interface_data
import pickle


class DndactiveCommand(Command):
    name: str = "dndactive"

    description: str = "Set a DnD character as active."

    aliases = ["da", "dnda", "active", "dactive"]

    syntax = "{name|id}"

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        identifier = args.optional(0)
        author = await data.get_author(error_if_none=True)
        active_character = await get_active_character(data)

        # Display the active character
        if identifier is None:
            if active_character is None:
                await data.reply("ℹ️ You haven't activated any character in this chat.")
            else:
                await data.reply(f"ℹ️ Your active character for this chat is [b]{active_character.character}[/b].")
            return

        # Find the character by name
        try:
            identifier = int(identifier)
        except ValueError:
            chars = await asyncify(data.session.query(self.alchemy.get(DndCharacter)).filter_by(name=identifier).all)
            if len(chars) >= 2:
                char_string = "\n".join([f"[c]{char.character_id}[/c] (LV {char.level}) by {char.creator})" for char in chars])
                raise CommandError(f"Multiple characters share the name {identifier}, "
                                   f"please activate them using their id:\n{char_string}")
            elif len(chars) == 1:
                char = chars[0]
            else:
                char = None
        else:
            # Find the character by id
            char = await asyncify(data.session.query(self.alchemy.get(DndCharacter))
                                              .filter_by(character_id=identifier)
                                              .one_or_none)
        if char is None:
            raise CommandError("No character found.")
        # Check if the player already has an active character
        if active_character is None:
            # Create a new active character
            achar = self.alchemy.get(DndActiveCharacter)(
                character=char,
                user=author,
                interface_name=self.interface.name,
                interface_data=pickle.dumps(get_interface_data(data)))
            data.session.add(achar)
        else:
            # Change the active character
            active_character.character = char
        await data.session_commit()
        await data.reply(f"✅ Active character set to [b]{char}[/b]!")
