from typing import *
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr
from .keipeople import KeiPerson

if TYPE_CHECKING:
    from royalnet.backpack.tables import User


class KeiUnlocks:
    __tablename__ = "keiunlocks"

    @declared_attr
    def unlocks_id(self) -> int:
        return Column(Integer, primary_key=True)

    @declared_attr
    def eris_id(self) -> str:
        return Column(String, ForeignKey("keipeople.kpid"))

    @declared_attr
    def eris(self) -> "KeiPerson":
        return relationship("KeiPerson", foreign_keys=self.eris_id)
