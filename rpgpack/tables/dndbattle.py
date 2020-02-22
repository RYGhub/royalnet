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

    def __repr__(self):
        return f"<{self.__class__.__qualname__} {self.name}>"

    def __str__(self):
        return f"{self.name}"

    def create_message(self):
        string = []
        string.append(f"⚔️ [b]{self.name}[/b]\n")
        string.append(f"{self.description}\n")
        return "".join(string)
