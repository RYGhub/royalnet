from typing import *
from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr

if TYPE_CHECKING:
    from royalnet.backpack.tables import User


class KeiPerson:
    __tablename__ = "keipeople"

    @declared_attr
    def kpid(self) -> str:
        return Column(String, primary_key=True)

    @declared_attr
    def user_id(self) -> Optional[int]:
        return Column(Integer, ForeignKey("users.uid"))

    @declared_attr
    def user(self) -> Optional["User"]:
        return relationship("User", foreign_keys=self.user_id, backref="kei_people")

    @declared_attr
    def name(self) -> Optional[str]:
        return Column(String)

    def __repr__(self):
        return f"<{self.__class__.__qualname__} {self.kpid}{' ' + self.user.username if self.user is not None else ''}>"

    def __str__(self):
        return self.user.username if self.user is not None else self.kpid
