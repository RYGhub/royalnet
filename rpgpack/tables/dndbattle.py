from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declared_attr


class DndBattle:
    __tablename__ = "dndbattle"

    @declared_attr
    def id(self):
        return Column(Integer, primary_key=True)

    @declared_attr
    def name(self):
        return Column(String, nullable=False)

    @declared_attr
    def description(self):
        return Column(String, nullable=False)
