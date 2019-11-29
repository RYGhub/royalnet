from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr


class KeiMessage:
    __tablename__ = "keimessages"

    @declared_attr
    def kmid(self):
        return Column(Integer, primary_key=True)

    @declared_attr
    def kei_person_id(self):
        return Column(String, ForeignKey("keipeople.kpid"), nullable=False)

    @declared_attr
    def kei_person(self):
        return relationship("KeiPerson", foreign_keys=self.kei_person_id, backref="kei_messages")

    @declared_attr
    def message(self):
        return Column(String, nullable=False)

    def __repr__(self):
        return f"<{self.__class__.__qualname__} '{self.message}'>"
