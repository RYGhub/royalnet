from typing import *
import royalnet
import royalnet.commands as rc
from ..types import Faction


class TestfactionCommand(rc.Command):
    name: str = "testfaction"

    description: str = "Test a faction string."

    syntax: str = "{factionstring}"

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        await data.reply(Faction[args[0].upper()].value)
