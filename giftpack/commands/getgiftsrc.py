from typing import *
from royalnet.commands import *
from .getgift import GetgiftCommand
from ..tables import XmasGift
from sqlalchemy.sql.expression import func


class GetgiftsrcCommand(GetgiftCommand):
    name: str = "getgiftsrc"

    aliases = ["drawgiftsrc"]

    description: str = "Estrai un regalo con un certo mittente."

    syntax: str = "{mittente}"

    async def _get_gift(self, args, data):
        return data.session.query(self.alchemy.get(XmasGift)).filter_by(drawn=False, source=args[0]).order_by(func.random()).first()
