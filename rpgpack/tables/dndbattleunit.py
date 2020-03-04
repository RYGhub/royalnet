from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declared_attr
from ..types import Health, Faction


class DndBattleUnit:
    __tablename__ = "dndbattleunit"

    @declared_attr
    def id(self):
        return Column(Integer, primary_key=True)

    @declared_attr
    def battle_id(self):
        return Column(Integer, ForeignKey("dndbattle.id"))

    @declared_attr
    def battle(self):
        return relationship("DndBattle", foreign_keys=self.battle_id, backref="units")

    @declared_attr
    def initiative(self):
        return Column(Integer, nullable=False)

    @declared_attr
    def health_string(self):
        return Column(String)

    @property
    def health(self):
        return Health.from_text(self.health_string) if self.health_string else None

    @health.setter
    def health(self, value: Health):
        self.health_string = value.to_text()

    @declared_attr
    def faction(self):
        return Column(Enum(Faction), nullable=False)

    @declared_attr
    def name(self):
        return Column(String, nullable=False)

    @declared_attr
    def armor_class(self):
        return Column(Integer)

    @declared_attr
    def extra(self):
        return Column(String)

    @declared_attr
    def status(self):
        return Column(String)

    def __str__(self):
        string = [
            f"{self.faction.value}",
            f"[b]{self.name}[/b]",
            f"[{self.initiative}]",
        ]

        if self.health:
            string.append(f"{self.health}")
        if self.armor_class:
            string.append(f"🛡 {self.armor_class}")
        if self.extra:
            string.append(f"💠 {self.extra}")
        if self.status:
            string.append(f"💫 {self.status}")
        return " ".join(string)

    def __repr__(self):
        return f"<DndBattleUnit {self.id} ({self.name})>"
