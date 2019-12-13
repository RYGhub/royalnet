from typing import *
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr


if TYPE_CHECKING:
    from .keipeople import KeiPerson


class KeiMessage:
    __tablename__ = "keimessages"

    @declared_attr
    def kmid(self) -> int:
        return Column(Integer, primary_key=True)

    @declared_attr
    def kei_person_id(self) -> str:
        return Column(String, ForeignKey("keipeople.kpid"), nullable=False)

    @declared_attr
    def kei_person(self) -> "KeiPerson":
        return relationship("KeiPerson", foreign_keys=self.kei_person_id, backref=backref("kei_messages",
                                                                                          cascade="all, delete-orphan"))

    @declared_attr
    def previous(self) -> Optional[str]:
        return Column(String)

    @declared_attr
    def message(self) -> str:
        return Column(String, nullable=False)

    def __repr__(self):
        return f"<{self.__class__.__qualname__} '{self.message}'>"
