from royalnet.commands import *
from ..tables import DndCharacter, DndActiveCharacter
from ..utils import get_active_character


class DndinfoCommand(Command):
    name: str = "dndinfo"

    description: str = "Display the character sheet of the active DnD character."

    aliases = ["di", "dndi", "info", "dinfo"]

    tables = {DndCharacter, DndActiveCharacter}

    _p_emoji = {
        0: "🌑",
        0.5: "🌗",
        1: "🌕",
        2: "⭐️",
    }

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        active_character = await get_active_character(data)

        if active_character is None:
            raise CommandError("You don't have an active character.")
        c: DndCharacter = active_character.character

        r = f"[b]{c.name}[/b]\n" \
            f"🔰 Lv. {c.level}\n" \
            f"\n" \
            f"❤️ {c.current_hp}/{c.max_hp}\n" \
            f"🛡 {c.armor_class}\n" \
            f"\n" \
            f"{self._p_emoji[c.strength_save_proficiency.value]} Strength: [b]{c.strength:+d}[/b] ({c.strength_score})\n" \
            f"{self._p_emoji[c.dexterity_save_proficiency.value]} Dexterity: [b]{c.dexterity:+d}[/b] ({c.dexterity_score})\n" \
            f"{self._p_emoji[c.constitution_save_proficiency.value]} Constitution: [b]{c.constitution:+d}[/b] ({c.constitution_score})\n" \
            f"{self._p_emoji[c.intelligence_save_proficiency.value]} Intelligence: [b]{c.intelligence:+d}[/b] ({c.intelligence_score})\n" \
            f"{self._p_emoji[c.wisdom_save_proficiency.value]} Wisdom: [b]{c.wisdom:+d}[/b] ({c.wisdom_score})\n" \
            f"{self._p_emoji[c.charisma_save_proficiency.value]} Charisma: [b]{c.charisma:+d}[/b] ({c.charisma_score})\n" \
            f"\n" \
            f"{self._p_emoji[c.acrobatics_proficiency.value]} Acrobatics: [b]{c.acrobatics:+d}[/b]\n" \
            f"{self._p_emoji[c.animal_handling_proficiency.value]} Animal Handling: [b]{c.animal_handling:+d}[/b]\n" \
            f"{self._p_emoji[c.arcana_proficiency.value]} Arcana: [b]{c.arcana:+d}[/b]\n" \
            f"{self._p_emoji[c.athletics_proficiency.value]} Athletics: [b]{c.athletics:+d}[/b]\n" \
            f"{self._p_emoji[c.deception_proficiency.value]} Deception: [b]{c.deception:+d}[/b]\n" \
            f"{self._p_emoji[c.history_proficiency.value]} History: [b]{c.history:+d}[/b]\n" \
            f"{self._p_emoji[c.insight_proficiency.value]} Insight: [b]{c.insight:+d}[/b]\n" \
            f"{self._p_emoji[c.intimidation_proficiency.value]} Intimidation: [b]{c.intimidation:+d}[/b]\n" \
            f"{self._p_emoji[c.investigation_proficiency.value]} Investigation: [b]{c.investigation:+d}[/b]\n" \
            f"{self._p_emoji[c.medicine_proficiency.value]} Medicine: [b]{c.medicine:+d}[/b]\n" \
            f"{self._p_emoji[c.nature_proficiency.value]} Nature: [b]{c.nature:+d}[/b]\n" \
            f"{self._p_emoji[c.perception_proficiency.value]} Perception: [b]{c.perception:+d}[/b]\n" \
            f"{self._p_emoji[c.performance_proficiency.value]} Performance: [b]{c.performance:+d}[/b]\n" \
            f"{self._p_emoji[c.persuasion_proficiency.value]} Persuasion: [b]{c.persuasion:+d}[/b]\n" \
            f"{self._p_emoji[c.religion_proficiency.value]} Religion: [b]{c.religion:+d}[/b]\n" \
            f"{self._p_emoji[c.sleight_of_hand_proficiency.value]} Sleight of Hand: [b]{c.sleight_of_hand:+d}[/b]\n" \
            f"{self._p_emoji[c.stealth_proficiency.value]} Stealth: [b]{c.stealth:+d}[/b]\n" \
            f"{self._p_emoji[c.survival_proficiency.value]} Survival: [b]{c.survival:+d}[/b]\n" \
            f"\n" \
            f"{self._p_emoji[c.initiative_proficiency.value]} Initiative: [b]{c.initiative:+d}[/b]\n"

        await data.reply(r)
