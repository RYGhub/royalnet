from typing import *
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declared_attr

if TYPE_CHECKING:
    from .wikirevision import WikiRevision


class WikiPage:
    __tablename__ = "wikipages"

    @declared_attr
    def page_id(self) -> int:
        return Column(Integer, primary_key=True)

    @declared_attr
    def latest_revision_id(self) -> int:
        return Column(Integer, ForeignKey("wikirevisions.revision_id"), nullable=False)

    @declared_attr
    def latest_revision(self) -> "WikiRevision":
        return relationship("WikiRevision", foreign_keys=self.latest_revision_id, uselist=False)
