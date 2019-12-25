from typing import *
from royalnet.commands import *
from royalnet.utils import *


class ExampleEvent(Event):
    name = "example"

    async def run(self, **kwargs) -> dict:
        return {"hello": "world"}
