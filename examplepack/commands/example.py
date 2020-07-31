from typing import *
from royalnet.commands import *
from royalnet.utils import *

# TODO: delete this file!


class ExampleCommand(Command):
    name: str = "example"

    description: str = "Say Hello to the world!"

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        await data.reply("Hello world!")
