from typing import *
from royalnet.commands import *
from ..tables import XmasGift
from sqlalchemy.sql.expression import func


class DelgiftCommand(Command):
    name: str = "delgift"

    description: str = "Elimina dal database il regalo con l'id specificato."

    syntax: str = ""

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        gift = data.session.query(self.alchemy.get(XmasGift)).filter_by(gift_id=int(args[0])).order_by(func.random()).first()
        data.session.delete(gift)
        await data.reply(f"🎁 Regalo eliminato (bye bye!):\n"
                         f"{gift}")
        await data.session_commit()
