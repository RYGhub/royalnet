import re

tags = {
    r"{@dice (.+?)(?:\|.*?)*}": r"🎲 [b]\1[/b]",
    r"{@scaledice (.+?)(?:\|.*?)*}": r"🎲 [b]\1[/b]",
    r"{@damage (.+?)(?:\|.*?)*}": r"⚔️ [b]\1[/b]",
    r"{@scaledamage (.+?)(?:\|.*?)*}": r"⚔️ [b]\1[/b]",
    r"{@condition (.+?)(?:\|.*?)*}": r"💫 [b]\1[/b]",
    r"{@creature (.+?)(?:\|.*?)*}": r"👤 [b]\1[/b]",
    r"{@spell (.+?)(?:\|.*?)*}": r"✨ [b]\1[/b]",
    r"{@sense (.+?)(?:\|.*?)*}": r"👁 [b]\1[/b]",
    r"{@item (.+?)(?:\|.*?)*}": r"📦 [b]\1[/b]",
    r"{@filter (.+?)(?:\|.*?)*}": r"\1",
    r"{@skill (.+?)(?:\|.*?)*}": r"🌕 [b]\1[/b]",
    r"{@action (.+?)(?:\|.*?)*}": r"🔰 [b]\1[/b]",
    r"{@note (.+?)(?:\|.*?)*}": r"[i]\1[/i]",
    r"{@chance (.+?)(?:\|.*?)*}": r"🎲 [b]\1%[/b]",
    r"{@b(?:old)? (.+?)(?:\|.*?)*}": r"[b]\1[/b]",
    r"{@i(?:talic)? (.+?)(?:\|.*?)*}": r"[i]\1[/i]",
    r"{@table (.+?)}(?:\|.*?)*": r"[i][table hidden][/i]",
    r"{@book (.+?)(?:\|.*?)*}": r"[i]\1[/i]",
    r"{@adventure (.+?)(?:\|.*?)*}": r"[i]\1[/i]",
    r"{@hit (.+?)(?:\|.*?)*}": r"🔸 [b]\1[/b]",
    r"{@hazard (.+?)(?:\|.*?)*}": r"⛈ [b]\1[/b]",
    r"{@atk rw}": r"[i]Ranged Weapon Attack[/i]",
    r"{@h}": r"[i]Hit:[/i]",
}

def parse_5etools_entry(entry) -> str:
    if isinstance(entry, str):
        result = entry
        for pattern in tags:
            result = re.sub(pattern, tags[pattern], result)
        return result
    elif isinstance(entry, dict):
        string = ""
        if entry["type"] == "entries":
            string += f'[b]{entry.get("name", "")}[/b]\n'
            for subentry in entry["entries"]:
                string += parse_5etools_entry(subentry)
                string += "\n\n"
        elif entry["type"] == "table":
            string += "[i][table hidden][/i]"
            # for label in entry["colLabels"]:
            #     string += f"| {label} "
            # string += "|"
            # for row in entry["rows"]:
            #     for column in row:
            #         string += f"| {self._parse_entry(column)} "
            #     string += "|\n"
        elif entry["type"] == "quote":
            return f"> {parse_5etools_entry(entry['entry'])}"
        elif entry["type"] == "cell":
            return parse_5etools_entry(entry["entry"])
        elif entry["type"] == "list":
            string = ""
            for item in entry["items"]:
                string += f"- {parse_5etools_entry(item)}\n"
            string.rstrip("\n")
        else:
            string += "[i]⚠️ [unknown type][/i]"
    else:
        return "[/i]⚠️ [unknown data][/i]"
    return string
