from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import *


class DndActiveBattle:
    __tablename__ = "dndactivebattle"

    @declared_attr
    def active_battle_id(self):
        return Column(Integer, primary_key=True)

    @declared_attr
    def battle_id(self):
        return Column(Integer, ForeignKey("dndbattle.id"))

    @declared_attr
    def battle(self):
        return relationship("DndBattle", foreign_keys=self.battle_id, backref=backref("activated_in"))

    @declared_attr
    def interface_name(self):
        return Column(String)

    @declared_attr
    def interface_data(self):
        return Column(LargeBinary)

    def __repr__(self):
        return f"<{self.__class__.__qualname__}: {self.battle_id}>"
