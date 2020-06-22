from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declared_attr
import datetime
import royalnet.utils as ru


class WikiDeletion:
    __tablename__ = "wikideletions"

    @declared_attr
    def page_id(self):
        return Column(Integer, primary_key=True)

    @declared_attr
    def deleted_by_id(self) -> int:
        return Column(Integer, ForeignKey("users.uid"), nullable=False)

    @declared_attr
    def deleted_by(self):
        return relationship("User", foreign_keys=self.deleted_by_id, backref="wiki_deletions")

    @declared_attr
    def timestamp(self) -> datetime.datetime:
        return Column(DateTime, nullable=False)

    def json(self) -> ru.JSON:
        return {
            "page_id": self.page_id,
            "deleted_by": self.deleted_by.json(),
            "timestamp": self.timestamp.isoformat(),
        }
