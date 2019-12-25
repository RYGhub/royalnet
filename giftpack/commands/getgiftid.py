from typing import *
from royalnet.commands import *
from .getgift import GetgiftCommand
from ..tables import XmasGift
from sqlalchemy.sql.expression import func


class GetgiftidCommand(GetgiftCommand):
    name: str = "getgiftid"

    aliases = ["drawgiftid"]

    description: str = "Estrai un regalo con un certo id."

    syntax: str = "{id}"

    async def _get_gift(self, args, data):
        return data.session.query(self.alchemy.get(XmasGift)).filter_by(drawn=False, gift_id=int(args[0])).order_by(func.random()).first()
