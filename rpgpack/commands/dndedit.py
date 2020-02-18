import re
from royalnet.commands import *
from .dndnew import DndnewCommand
from ..tables import DndCharacter
from ..utils import get_active_character


class DndeditCommand(DndnewCommand):
    name: str = "dndedit"

    description: str = "Edit the active DnD character."

    aliases = ["de", "dnde", "edit", "dedit"]

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        character_sheet = args.joined()

        if character_sheet == "":
            await data.reply(self._syntax())
            return

        active_character = await get_active_character(data)
        if active_character is None:
            raise CommandError("You don't have an active character.")
        char = active_character.character

        arguments = self._parse(character_sheet)
        for key in arguments:
            char.__setattr__(key, arguments[key])

        await data.session_commit()

        await data.reply(f"✅ Edit successful!")
