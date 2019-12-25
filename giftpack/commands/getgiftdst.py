from typing import *
from royalnet.commands import *
from .getgift import GetgiftCommand
from ..tables import XmasGift
from sqlalchemy.sql.expression import func


class GetgiftdstCommand(GetgiftCommand):
    name: str = "getgiftdst"

    aliases = ["drawgiftdst"]

    description: str = "Estrai un regalo con un certo destinatario."

    syntax: str = "{destinatario}"

    async def _get_gift(self, args, data):
        return data.session.query(self.alchemy.get(XmasGift)).filter_by(drawn=False, destination=args[0]).order_by(func.random()).first()
