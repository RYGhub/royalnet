from typing import *
from royalnet.commands import *
from royalnet.utils import *
from ..tables import XmasGift
from sqlalchemy.sql.expression import func


class GetgiftCommand(Command):
    name = "getgift"

    aliases = ["drawgift"]

    description = "Estrai un regalo qualsiasi."

    async def _get_gift(self, args, data):
        # Requires postgres
        return data.session.query(self.alchemy.get(XmasGift)).filter_by(drawn=False).order_by(func.random()).first()

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        xmasgift = await self._get_gift(args, data)
        if xmasgift is None:
            raise CommandError("Nessun regalo sorteggiabile.")

        await data.reply(f"🎁 Il prossimo regalo è...\n"
                         f"{xmasgift}!")

        xmasgift.drawn = True
        await data.session_commit()
