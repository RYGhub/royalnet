from typing import *
from royalnet.commands import *
from ..tables import XmasGift


class ListgiftsCommand(Command):
    name: str = "listgifts"

    aliases = ["listgift"]

    description: str = "Elenca tutti i regali registrati."

    syntax: str = ""

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        gifts = data.session.query(self.alchemy.get(XmasGift)).all()
        msg = "🎁 Elenco regali:\n"
        gift_msg = "\n".join([str(gift) for gift in gifts])
        await data.reply(msg + gift_msg)
