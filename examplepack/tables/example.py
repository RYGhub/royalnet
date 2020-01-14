from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declared_attr


class Example:
    __tablename__ = "examples"

    @declared_attr
    def creator_id(self):
        return Column(Integer, ForeignKey("users.uid"), primary_key=True)

    @declared_attr
    def creator(self):
        return relationship("User", backref=backref("examples_createdx"))

    @declared_attr
    def example(self):
        return Column(String, nullable=False, default="Hello world!")
