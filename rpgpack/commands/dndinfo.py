from royalnet.commands import *
from ..tables import DndCharacter, DndActiveCharacter
from ..utils import get_active_character


class DndinfoCommand(Command):
    name: str = "dndinfo"

    description: str = "Display the character sheet of the active DnD character."

    aliases = ["di", "dndi", "info", "dinfo"]

    tables = {DndCharacter, DndActiveCharacter}

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        active_character = await get_active_character(data)
        char = active_character.character

        if char is None:
            raise CommandError("You don't have an active character.")
        await data.reply(char.character_sheet())
