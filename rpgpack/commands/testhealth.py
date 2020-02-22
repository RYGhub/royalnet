from typing import *
import royalnet
import royalnet.commands as rc
from ..types import Health


class TesthealthCommand(rc.Command):
    name: str = "testhealth"

    description: str = "Test a health string."

    syntax: str = "{healthstring}"

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        await data.reply(str(Health.from_text(args[0])))
