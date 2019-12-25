from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declared_attr


class XmasGift:
    __tablename__ = "xmasgifts"

    @declared_attr
    def gift_id(self):
        return Column(Integer, primary_key=True)

    @declared_attr
    def source(self):
        return Column(String, nullable=False)

    @declared_attr
    def destination(self):
        return Column(String, nullable=False)

    @declared_attr
    def extra_text(self):
        return Column(String, nullable=False, default="")

    @declared_attr
    def drawn(self):
        return Column(Boolean, nullable=False, default=False)

    def __str__(self):
        msg = f"Regalo #{self.gift_id} da {self.source} a {self.destination}" + (f": {self.extra_text}" if self.extra_text else "")
        if self.drawn:
            return f"⚫️ {msg}"
        else:
            return f"🔵 [b]{msg}[/b]"
