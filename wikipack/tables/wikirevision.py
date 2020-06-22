from typing import *
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import *
import royalnet.utils as ru
import datetime


if TYPE_CHECKING:
    from royalnet.backpack.tables import User


class WikiRevision:
    __tablename__ = "wikirevisions"

    @declared_attr
    def page_id(self) -> int:
        return Column(Integer, Sequence('wikirevision_page_id_seq'), primary_key=True)

    @declared_attr
    def revision_id(self) -> int:
        return Column(Integer, Sequence('wikirevision_revision_id_seq'), primary_key=True)

    @declared_attr
    def category(self) -> str:
        return Column(String, nullable=False)

    @declared_attr
    def title(self) -> str:
        return Column(String, nullable=False)

    @declared_attr
    def contents(self) -> str:
        return Column(Text, nullable=False)

    @declared_attr
    def format(self) -> str:
        # GitHub Flavored Markdown
        # https://github.github.com/gfm/
        return Column(String, nullable=False, default="gfm")

    @declared_attr
    def author_id(self) -> int:
        return Column(Integer, ForeignKey("users.uid"), nullable=False)

    @declared_attr
    def author(self) -> "User":
        return relationship("User", foreign_keys=self.author_id, backref="wiki_revisions")

    @declared_attr
    def timestamp(self) -> datetime.datetime:
        return Column(DateTime, nullable=False)

    @declared_attr
    def role_to_view(self) -> str:
        return Column(String)

    @declared_attr
    def role_to_edit(self) -> str:
        return Column(String)

    def json_list(self):
        return {
            "page_id": self.page_id,
            "category": self.category,
            "title": self.title,
            "role_to_view": self.role_to_view,
        }

    def json(self) -> ru.JSON:
        return {
            "page_id": self.page_id,
            "revision_id": self.revision_id,
            "category": self.category,
            "title": self.title,
            "contents": self.contents,
            "format": self.format,
            "author": self.author.json(),
            "timestamp": self.timestamp.isoformat(),
            "role_to_view": self.role_to_view,
            "role_to_edit": self.role_to_edit,
        }
