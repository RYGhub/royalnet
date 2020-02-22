import aiohttp
import sortedcontainers
import logging
from royalnet.commands import *
from royalnet.utils import sentry_exc
from ..utils import parse_5etools_entry


log = logging.getLogger(__name__)


class DnditemCommand(Command):
    name: str = "dnditem"

    aliases = ["item"]

    description: str = "Ottieni informazioni su un oggetto di D&D5e."

    syntax = "{nomeoggetto}"

    _dnddata: sortedcontainers.SortedKeyList = None

    def __init__(self, interface: CommandInterface):
        super().__init__(interface)
        self.loop.create_task(self._fetch_dnddata())

    async def _fetch_dnddata(self):
        self._dnddata = self._dnddata = sortedcontainers.SortedKeyList([], key=lambda i: i["name"].lower())
        async with aiohttp.ClientSession() as session:
            async with session.get("https://5e.tools/data/items.json") as response:
                j = await response.json()
                for item in j["item"]:
                    self._dnddata.add(item)
            async with session.get("https://5e.tools/data/fluff-items.json") as response:
                j = await response.json()
                for item in j["itemFluff"]:
                    self._dnddata.add(item)
            async with session.get("https://5e.tools/data/items-base.json") as response:
                j = await response.json()
                for item in j["baseitem"]:
                    self._dnddata.add(item)
        self._test_all()

    @staticmethod
    def _parse_item(item: dict) -> str:
        string = [f'📦 [b]{item["name"]}[/b]\n']

        # Source (manual, page)
        if "source" in item:
            if "page" in item:
                string.append(f'[i]{item["source"]}, page {item["page"]}[/i]\n')
            else:
                string.append(f'[i]{item["source"]}[/i]\n')
        string.append("\n")

        # Type
        item_type = item.get("type")
        if item_type:
            string.append(f"Type: [b]{item_type}[/b]\n")

        # Value
        item_value = item.get("value")
        if item_value:
            string.append(f"Value: [b]{item_value}[/b]\n")

        # Weight
        item_weight = item.get("weight")
        if item_weight:
            string.append(f"Value: [b]{item_weight}[/b]\n")

        # Rarity
        item_rarity = item.get("rarity")
        if item_rarity:
            string.append(f"Rarity: [b]{item_rarity}[/b]\n")
        else:
            string.append(f"Rarity: [b]Mundane[/b]\n")

        string.append("\n")

        # Text entries
        for entry in item.get("entries", []):
            string += parse_5etools_entry(entry)
            string += "\n\n"

        return "".join(string)

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        if self._dnddata is None:
            await data.reply("⚠️ Il database degli oggetti di D&D non è ancora stato scaricato.")
            return
        search = args.joined().lower()
        result = self._dnddata[self._dnddata.bisect_key_left(search)]
        await data.reply(self._parse_item(result))

    def _test_all(self):
        for item in self._dnddata:
            try:
                log.debug(f"Testing: {item['name']}")
                self._parse_item(item)
            except Exception as e:
                log.error(f"Failed: {item['name']}")
                sentry_exc(e)
                breakpoint()
        log.info(f"All item tests complete!")
