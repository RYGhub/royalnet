import aiohttp
import sortedcontainers
import logging
from royalnet.commands import *
from royalnet.utils import ordinalformat, andformat, sentry_exc
from ..utils import parse_5etools_entry


log = logging.getLogger(__name__)


class DndspellCommand(Command):
    name: str = "dndspell"

    aliases = ["spell"]

    description: str = "Ottieni informazioni su una magia di D&D5e."

    syntax = "{nomemagia}"

    _dnddata: sortedcontainers.SortedKeyList = None

    def __init__(self, interface: CommandInterface):
        super().__init__(interface)
        interface.loop.create_task(self._fetch_dnddata())

    async def _fetch_dnddata(self):
        self._dnddata = self._dnddata = sortedcontainers.SortedKeyList([], key=lambda i: i["name"].lower())
        async with aiohttp.ClientSession() as session:
            for url in [
                "https://5e.tools/data/spells/spells-ai.json",
                "https://5e.tools/data/spells/spells-ggr.json",
                "https://5e.tools/data/spells/spells-phb.json",
                "https://5e.tools/data/spells/spells-scag.json",
                "https://5e.tools/data/spells/spells-xge.json",
                "https://5e.tools/data/spells/spells-ua-frw.json",
                "https://5e.tools/data/spells/spells-stream.json",
                "https://5e.tools/data/spells/spells-llk.json",
                "https://5e.tools/data/spells/spells-ua-saw.json",
                "https://5e.tools/data/spells/spells-ua-mm.json",
                "https://5e.tools/data/spells/spells-ua-ss.json",
                "https://5e.tools/data/spells/spells-ua-tobm.json",
                "https://5e.tools/data/spells/spells-ua-ar.json",
            ]:
                async with session.get(url) as response:
                    j = await response.json()
                    for spell in j["spell"]:
                        self._dnddata.add(spell)
        self._test_all()

    @staticmethod
    def _parse_spell(spell: dict) -> str:
        string = [f'✨ [b]{spell["name"]}[/b]\n']

        # Source (manual, page)
        if "source" in spell:
            if "page" in spell:
                string.append(f'[i]{spell["source"]}, page {spell["page"]}[/i]\n')
            else:
                string.append(f'[i]{spell["source"]}[/i]\n')
        string.append("\n")

        # Level
        string.append({
            0: "0️⃣ [b]Cantrip[/b]\n",
            1: "1️⃣ [b]1st[/b] level\n",
            2: "2️⃣ [b]2nd[/b] level\n",
            3: "3️⃣ [b]3rd[/b] level\n",
            4: "4️⃣ [b]4th[/b] level\n",
            5: "5️⃣ [b]5th[/b] level\n",
            6: "6️⃣ [b]6th[/b] level\n",
            7: "7️⃣ [b]7th[/b] level\n",
            8: "8️⃣ [b]8th[/b] level\n",
            9: "9️⃣ [b]9th[/b] level\n",
        }[spell["level"]])

        # School
        string.append({
            "A": "Abjuration",
            "C": "Conjuration",
            "D": "Divination",
            "E": "Enchantment",
            "V": "Evocation",
            "I": "Illusion",
            "N": "Necromancy",
            "P": "Psionic",
            "T": "Transmutation",
        }[spell["school"]])
        string.append("\n\n")

        # Cast time
        for time in spell.get("time", []):
            string.append(f'Cast time: ⌛️ [b]{time["number"]} {time["unit"]}[/b]\n')

        # Cast range
        range = spell.get("range")
        if range:
            if range["type"] == "point":
                distance = range["distance"]
                if distance["type"] == "touch":
                    string.append("Range: 👉 [b]Touch[/b]\n")
                elif distance["type"] == "self":
                    string.append("Range: 👤 [b]Self[/b]\n")
                elif distance["type"] == "sight":
                    string.append("Range: 👁 [b]Sight[/b]\n")
                elif distance["type"] == "unlimited":
                    string.append("Range: ♾ [b]Unlimited[/b]\n")
                else:
                    string.append(f'Range: 🏹 [b]{spell["range"]["distance"]["amount"]}'
                                  f' {spell["range"]["distance"]["type"]}[/b] (point)\n')
            elif range["type"] == "radius":
                string.append(f'Range: ⭕️ [b]{spell["range"]["distance"]["amount"]}'
                              f' {spell["range"]["distance"]["type"]}[/b] (radius)\n')
            elif range["type"] == "sphere":
                string.append(f'Range: 🌕 [b]{spell["range"]["distance"]["amount"]}'
                              f' {spell["range"]["distance"]["type"]}[/b] (sphere)\n')
            elif range["type"] == "cone":
                string.append(f'Range: 🍦 [b]{spell["range"]["distance"]["amount"]}'
                              f' {spell["range"]["distance"]["type"]}[/b] (cone)\n')
            elif range["type"] == "line":
                string.append(f'Range: ➖ [b]{spell["range"]["distance"]["amount"]}'
                              f' {spell["range"]["distance"]["type"]}[/b] (line)\n')
            elif range["type"] == "hemisphere":
                string.append(f'Range: 🌗 [b]{spell["range"]["distance"]["amount"]}'
                              f' {spell["range"]["distance"]["type"]}[/b] (hemisphere)\n')
            elif range["type"] == "cube":
                string.append(f'Range: ⬜️ [b]{spell["range"]["distance"]["amount"]}'
                              f' {spell["range"]["distance"]["type"]}[/b] (cube)\n')
            elif range["type"] == "special":
                string.append("Range: ⭐️ Special")
            else:
                string.append('Range: ⚠️[b]UNKNOWN[/b]')

        # Components
        components = spell.get("components")
        if components:
            string.append(f'Components: ')
            if components.get("v", False):
                string.append("👄 [b]Verbal[/b] | ")
            if components.get("s", False):
                string.append("🤙 [b]Somatic[/b] | ")
            if components.get("r", False):
                string.append("©️ [b]Royalty[/b] | ")
            if components.get("m", False):
                if isinstance(components["m"], dict):
                    string.append(f'💎 [b]Material[/b] ([i]{spell["components"]["m"]["text"]}[/i]) | ')
                elif isinstance(components["m"], str):
                    string.append(f'💎 [b]Material[/b] ([i]{spell["components"]["m"]}[/i]) | ')
            string[-1] = string[-1].replace(" | ", "\n")
        string.append("\n")

        # Durations
        for duration in spell.get("duration", []):
            if duration["type"] == "timed":
                string.append(f'Duration: 🕒 [b]{duration["duration"]["amount"]} {duration["duration"]["type"]}[/b]')
            elif duration["type"] == "instant":
                string.append('Duration: ☁️ [b]Instantaneous[/b]')
            elif duration["type"] == "special":
                string.append('Duration: ⭐️ [b]Special[/b]')
            elif duration["type"] == "permanent":
                string.append(f"Duration: ♾ [b]Permanent[/b] (ends on {andformat(duration['ends'], final=' or ')})")
            else:
                string.append(f'Duration: ⚠️[b]UNKNOWN[/b]')
            if duration.get("concentration", False):
                string.append(" (requires 🧠 Concentration)")
            string.append("\n")

        # Extra data
        meta = spell.get("meta")
        if meta:
            if meta.get("ritual", False):
                string.append("🔮 Can be casted as ritual\n")
        string.append("\n")

        # Text entries
        for entry in spell.get("entries", []):
            string.append(parse_5etools_entry(entry))
            string.append("\n\n")

        # At an higher level... text entries
        for entry in spell.get("entriesHigherLevel", []):
            string.append(parse_5etools_entry(entry))
            string.append("\n\n")

        return "".join(string)

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        if self._dnddata is None:
            await data.reply("⚠️ Il database degli oggetti di D&D non è ancora stato scaricato.")
            return
        search = args.joined().lower()
        result = self._dnddata[self._dnddata.bisect_key_left(search)]
        await data.reply(self._parse_spell(result))

    def _test_all(self):
        for spell in self._dnddata:
            try:
                log.debug(f"Testing: {spell['name']}")
                self._parse_spell(spell)
            except Exception as e:
                log.error(f"Failed: {spell['name']}")
                sentry_exc(e)
        log.info(f"All spell tests complete!")
