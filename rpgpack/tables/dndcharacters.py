import math
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import *
from ..types import DndProficiencyType
from royalnet.utils import JSON


class DndCharacter:
    __tablename__ = "dndcharacters"

    @declared_attr
    def character_id(self):
        return Column(Integer, primary_key=True)

    @declared_attr
    def creator_id(self):
        return Column(Integer, ForeignKey("users.uid"))

    @declared_attr
    def creator(self):
        return relationship("User", foreign_keys=self.creator_id, backref="dndcharacters_created")

    @declared_attr
    def name(self):
        return Column(String, nullable=False)

    @declared_attr
    def strength_score(self):
        return Column(Integer, nullable=False)

    @property
    def strength(self):
        return (self.strength_score - 10) // 2

    @declared_attr
    def dexterity_score(self):
        return Column(Integer, nullable=False)

    @property
    def dexterity(self):
        return (self.dexterity_score - 10) // 2

    @declared_attr
    def constitution_score(self):
        return Column(Integer, nullable=False)

    @property
    def constitution(self):
        return (self.constitution_score - 10) // 2

    @declared_attr
    def intelligence_score(self):
        return Column(Integer, nullable=False)

    @property
    def intelligence(self):
        return (self.intelligence_score - 10) // 2

    @declared_attr
    def wisdom_score(self):
        return Column(Integer, nullable=False)

    @property
    def wisdom(self):
        return (self.wisdom_score - 10) // 2

    @declared_attr
    def charisma_score(self):
        return Column(Integer, nullable=False)

    @property
    def charisma(self):
        return (self.charisma_score - 10) // 2

    @declared_attr
    def level(self):
        return Column(Integer, nullable=False)

    @property
    def proficiency_bonus(self):
        return ((self.level - 1) // 4) + 2

    @declared_attr
    def current_hp(self):
        return Column(Integer, nullable=False)

    @declared_attr
    def max_hp(self):
        return Column(Integer, nullable=False)

    @declared_attr
    def armor_class(self):
        return Column(Integer, nullable=False)

    @declared_attr
    def strength_save_proficiency(self):
        return Column(Enum(DndProficiencyType), nullable=False, default=DndProficiencyType.NONE)

    @declared_attr
    def dexterity_save_proficiency(self):
        return Column(Enum(DndProficiencyType), nullable=False, default=DndProficiencyType.NONE)

    @declared_attr
    def constitution_save_proficiency(self):
        return Column(Enum(DndProficiencyType), nullable=False, default=DndProficiencyType.NONE)

    @declared_attr
    def intelligence_save_proficiency(self):
        return Column(Enum(DndProficiencyType), nullable=False, default=DndProficiencyType.NONE)

    @declared_attr
    def wisdom_save_proficiency(self):
        return Column(Enum(DndProficiencyType), nullable=False, default=DndProficiencyType.NONE)

    @declared_attr
    def charisma_save_proficiency(self):
        return Column(Enum(DndProficiencyType), nullable=False, default=DndProficiencyType.NONE)

    @declared_attr
    def acrobatics_proficiency(self):
        return Column(Enum(DndProficiencyType), nullable=False, default=DndProficiencyType.NONE)

    @declared_attr
    def animal_handling_proficiency(self):
        return Column(Enum(DndProficiencyType), nullable=False, default=DndProficiencyType.NONE)

    @declared_attr
    def arcana_proficiency(self):
        return Column(Enum(DndProficiencyType), nullable=False, default=DndProficiencyType.NONE)

    @declared_attr
    def athletics_proficiency(self):
        return Column(Enum(DndProficiencyType), nullable=False, default=DndProficiencyType.NONE)

    @declared_attr
    def deception_proficiency(self):
        return Column(Enum(DndProficiencyType), nullable=False, default=DndProficiencyType.NONE)

    @declared_attr
    def history_proficiency(self):
        return Column(Enum(DndProficiencyType), nullable=False, default=DndProficiencyType.NONE)

    @declared_attr
    def insight_proficiency(self):
        return Column(Enum(DndProficiencyType), nullable=False, default=DndProficiencyType.NONE)

    @declared_attr
    def intimidation_proficiency(self):
        return Column(Enum(DndProficiencyType), nullable=False, default=DndProficiencyType.NONE)

    @declared_attr
    def investigation_proficiency(self):
        return Column(Enum(DndProficiencyType), nullable=False, default=DndProficiencyType.NONE)

    @declared_attr
    def medicine_proficiency(self):
        return Column(Enum(DndProficiencyType), nullable=False, default=DndProficiencyType.NONE)

    @declared_attr
    def nature_proficiency(self):
        return Column(Enum(DndProficiencyType), nullable=False, default=DndProficiencyType.NONE)

    @declared_attr
    def perception_proficiency(self):
        return Column(Enum(DndProficiencyType), nullable=False, default=DndProficiencyType.NONE)

    @declared_attr
    def performance_proficiency(self):
        return Column(Enum(DndProficiencyType), nullable=False, default=DndProficiencyType.NONE)

    @declared_attr
    def persuasion_proficiency(self):
        return Column(Enum(DndProficiencyType), nullable=False, default=DndProficiencyType.NONE)

    @declared_attr
    def religion_proficiency(self):
        return Column(Enum(DndProficiencyType), nullable=False, default=DndProficiencyType.NONE)

    @declared_attr
    def sleight_of_hand_proficiency(self):
        return Column(Enum(DndProficiencyType), nullable=False, default=DndProficiencyType.NONE)

    @declared_attr
    def stealth_proficiency(self):
        return Column(Enum(DndProficiencyType), nullable=False, default=DndProficiencyType.NONE)

    @declared_attr
    def survival_proficiency(self):
        return Column(Enum(DndProficiencyType), nullable=False, default=DndProficiencyType.NONE)

    @declared_attr
    def initiative_proficiency(self):
        return Column(Enum(DndProficiencyType), nullable=False, default=DndProficiencyType.NONE)

    @property
    def strength_save(self):
        return self.strength + math.floor(self.proficiency_bonus * self.strength_save_proficiency.value)

    @property
    def dexterity_save(self):
        return self.dexterity + math.floor(self.proficiency_bonus * self.dexterity_save_proficiency.value)

    @property
    def constitution_save(self):
        return self.constitution + math.floor(self.proficiency_bonus * self.constitution_save_proficiency.value)

    @property
    def intelligence_save(self):
        return self.intelligence + math.floor(self.proficiency_bonus * self.intelligence_save_proficiency.value)

    @property
    def wisdom_save(self):
        return self.wisdom + math.floor(self.proficiency_bonus * self.wisdom_save_proficiency.value)

    @property
    def charisma_save(self):
        return self.charisma + math.floor(self.proficiency_bonus * self.charisma_save_proficiency.value)

    @property
    def acrobatics(self):
        return self.dexterity + math.floor(self.proficiency_bonus * self.acrobatics_proficiency.value)

    @property
    def animal_handling(self):
        return self.wisdom + math.floor(self.proficiency_bonus * self.animal_handling_proficiency.value)

    @property
    def arcana(self):
        return self.intelligence + math.floor(self.proficiency_bonus * self.arcana_proficiency.value)

    @property
    def athletics(self):
        return self.strength + math.floor(self.proficiency_bonus * self.athletics_proficiency.value)

    @property
    def deception(self):
        return self.charisma + math.floor(self.proficiency_bonus * self.deception_proficiency.value)

    @property
    def history(self):
        return self.intelligence + math.floor(self.proficiency_bonus * self.history_proficiency.value)

    @property
    def insight(self):
        return self.wisdom + math.floor(self.proficiency_bonus * self.insight_proficiency.value)

    @property
    def intimidation(self):
        return self.charisma + math.floor(self.proficiency_bonus * self.intimidation_proficiency.value)

    @property
    def investigation(self):
        return self.intelligence + math.floor(self.proficiency_bonus * self.investigation_proficiency.value)

    @property
    def medicine(self):
        return self.wisdom + math.floor(self.proficiency_bonus * self.medicine_proficiency.value)

    @property
    def nature(self):
        return self.intelligence + math.floor(self.proficiency_bonus * self.nature_proficiency.value)

    @property
    def perception(self):
        return self.wisdom + math.floor(self.proficiency_bonus * self.perception_proficiency.value)

    @property
    def performance(self):
        return self.charisma + math.floor(self.proficiency_bonus * self.performance_proficiency.value)

    @property
    def persuasion(self):
        return self.charisma + math.floor(self.proficiency_bonus * self.persuasion_proficiency.value)

    @property
    def religion(self):
        return self.intelligence + math.floor(self.proficiency_bonus * self.religion_proficiency.value)

    @property
    def sleight_of_hand(self):
        return self.dexterity + math.floor(self.proficiency_bonus * self.sleight_of_hand_proficiency.value)

    @property
    def stealth(self):
        return self.dexterity + math.floor(self.proficiency_bonus * self.stealth_proficiency.value)

    @property
    def survival(self):
        return self.wisdom + math.floor(self.proficiency_bonus * self.survival_proficiency.value)

    @property
    def initiative(self):
        return self.dexterity + math.floor(self.proficiency_bonus * self.initiative_proficiency.value)

    def __repr__(self):
        return f"<{self.__class__.__qualname__} {self.name}>"

    def __str__(self):
        return f"{self.name}"

    def character_sheet(self) -> str:
        columns = list(self.__class__.__table__.columns)
        column_names = [column.name for column in columns if (not column.primary_key and
                                                              not column.foreign_keys and
                                                              column.name != "name")]
        message = f"[b]{self.name}[/b]\n"
        for column_name in column_names:
            value = self.__getattribute__(column_name)
            message += f"{column_name} {value}\n"
        return message

    def json(self) -> JSON:
        return {
            "creator": self.creator.json() if self.creator else None,
            "name": self.name,
            "level": self.level,
            "hp": {
                "current": self.current_hp,
                "max": self.max_hp
            },
            "armor_class": self.armor_class,
            "strength": {
                "score": self.strength_score,
                "modifier": self.strength,
                "save": self.strength_save,
                "save_proficiency": self.strength_save_proficiency.value
            },
            "dexterity": {
                "score": self.dexterity_score,
                "modifier": self.dexterity,
                "save": self.dexterity_save,
                "save_proficiency": self.dexterity_save_proficiency.value
            },
            "constitution": {
                "score": self.constitution_score,
                "modifier": self.constitution,
                "save": self.constitution_save,
                "save_proficiency": self.constitution_save_proficiency.value
            },
            "intelligence": {
                "score": self.intelligence_score,
                "modifier": self.intelligence,
                "save": self.intelligence_save,
                "save_proficiency": self.intelligence_save_proficiency.value
            },
            "wisdom": {
                "score": self.wisdom_score,
                "modifier": self.wisdom,
                "save": self.wisdom_save,
                "save_proficiency": self.wisdom_save_proficiency.value
            },
            "charisma": {
                "score": self.charisma_score,
                "modifier": self.charisma,
                "save": self.charisma_save,
                "save_proficiency": self.charisma_save_proficiency.value
            },
            "acrobatics": {
                "modifier": self.acrobatics,
                "proficiency": self.acrobatics_proficiency.value
            },
            "animal_handling": {
                "modifier": self.animal_handling,
                "proficiency": self.animal_handling_proficiency.value
            },
            "arcana": {
                "modifier": self.arcana,
                "proficiency": self.arcana_proficiency.value
            },
            "athletics": {
                "modifier": self.athletics,
                "proficiency": self.athletics_proficiency.value
            },
            "deception": {
                "modifier": self.deception,
                "proficiency": self.deception_proficiency.value
            },
            "history": {
                "modifier": self.history,
                "proficiency": self.history_proficiency.value
            },
            "insight": {
                "modifier": self.insight,
                "proficiency": self.insight_proficiency.value
            },
            "intimidation": {
                "modifier": self.intimidation,
                "proficiency": self.intimidation_proficiency.value
            },
            "investigation": {
                "modifier": self.investigation,
                "proficiency": self.investigation_proficiency.value
            },
            "medicine": {
                "modifier": self.medicine,
                "proficiency": self.medicine_proficiency.value
            },
            "nature": {
                "modifier": self.nature,
                "proficiency": self.nature_proficiency.value
            },
            "perception": {
                "modifier": self.perception,
                "proficiency": self.perception_proficiency.value
            },
            "performance": {
                "modifier": self.performance,
                "proficiency": self.performance_proficiency.value
            },
            "persuasion": {
                "modifier": self.persuasion,
                "proficiency": self.persuasion_proficiency.value
            },
            "religion": {
                "modifier": self.religion,
                "proficiency": self.religion_proficiency.value
            },
            "sleight_of_hand": {
                "modifier": self.sleight_of_hand,
                "proficiency": self.sleight_of_hand_proficiency.value
            },
            "stealth": {
                "modifier": self.stealth,
                "proficiency": self.stealth_proficiency.value
            },
            "survival": {
                "modifier": self.survival,
                "proficiency": self.survival_proficiency.value
            },
            "initiative": {
                "modifier": self.initiative,
                "proficiency": self.initiative_proficiency.value
            }
        }
