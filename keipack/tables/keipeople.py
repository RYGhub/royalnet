from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr


class KeiPerson:
    __tablename__ = "keipeople"

    @declared_attr
    def user_id(self):
        return Column(Integer, ForeignKey("users.uid"), primary_key=True)

    @declared_attr
    def user(self):
        return relationship("User", foreign_keys=self.user_id, backref="kei_people")

    @declared_attr
    def game_id(self):
        return Column(String, unique=True, primary_key=True)
