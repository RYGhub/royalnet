from typing import *
from royalnet.commands import *
from royalnet.utils import *
from ..tables import XmasGift


class AddgiftCommand(Command):
    name: str = "addgift"

    aliases = ["newgift"]

    description: str = "Aggiungi un nuovo regalo al pool."

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        source = args[0]
        destination = args[1]
        extra_text = " ".join(args[2:])

        xmasgift = self.alchemy.get(XmasGift)(
            source=source,
            destination=destination,
            extra_text=extra_text,
        )

        data.session.add(xmasgift)
        await data.session_commit()

        await data.reply(f"🎁 Regalo creato:\n"
                         f"{xmasgift}")
