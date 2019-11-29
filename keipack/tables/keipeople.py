from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr


class KeiPerson:
    __tablename__ = "keipeople"

    @declared_attr
    def kpid(self):
        return Column(String, primary_key=True)

    @declared_attr
    def user_id(self):
        return Column(Integer, ForeignKey("users.uid"))

    @declared_attr
    def user(self):
        return relationship("User", foreign_keys=self.user_id, backref="kei_people")

    def __repr__(self):
        return f"<{self.__class__.__qualname__} {self.kpid}{' ' + self.user.username if self.user is not None else ''}>"
