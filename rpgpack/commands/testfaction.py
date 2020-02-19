from typing import *
import royalnet
import royalnet.commands as rc
from ..utils import FactionColor


class TestfactionCommand(rc.Command):
    name: str = "testfaction"

    description: str = "Test a faction string."

    syntax: str = "{factionstring}"

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        await data.reply(FactionColor[args[0].upper()].value)
