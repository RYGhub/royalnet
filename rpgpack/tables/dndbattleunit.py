from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declared_attr
from ..utils import Health, Faction


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
        return relationship("DndBattle", backref="units")

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
