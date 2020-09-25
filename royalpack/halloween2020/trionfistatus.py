from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr
from .trionfilist import trionfilist


class TrionfiStatus:
    __tablename__ = "trionfistatus"

    @declared_attr
    def _steamid(self):
        return Column(BigInteger, ForeignKey("steam._steamid"), primary_key=True)

    @declared_attr
    def steam(self):
        return relationship("Steam", backref=backref("trionfistatus", uselist=False))

    @declared_attr
    def zero(self):
        return Column(DateTime)

    @declared_attr
    def i(self):
        return Column(DateTime)

    @declared_attr
    def ii(self):
        return Column(DateTime)

    @declared_attr
    def iii(self):
        return Column(DateTime)

    @declared_attr
    def iv(self):
        return Column(DateTime)

    @declared_attr
    def v(self):
        return Column(DateTime)

    @declared_attr
    def vi(self):
        return Column(DateTime)

    @declared_attr
    def vii(self):
        return Column(DateTime)

    @declared_attr
    def viii(self):
        return Column(DateTime)

    @declared_attr
    def ix(self):
        return Column(DateTime)

    @declared_attr
    def x(self):
        return Column(DateTime)

    @declared_attr
    def xi(self):
        return Column(DateTime)

    @declared_attr
    def xii(self):
        return Column(DateTime)

    @declared_attr
    def xiii(self):
        return Column(DateTime)

    @declared_attr
    def xiv(self):
        return Column(DateTime)

    @declared_attr
    def xv(self):
        return Column(DateTime)

    @declared_attr
    def xvi(self):
        return Column(DateTime)

    @declared_attr
    def xvii(self):
        return Column(DateTime)

    @declared_attr
    def xviii(self):
        return Column(DateTime)

    @declared_attr
    def xix(self):
        return Column(DateTime)

    @declared_attr
    def xx(self):
        return Column(DateTime)

    @declared_attr
    def xxi(self):
        return Column(DateTime)

    def total(self):
        return sum(map(lambda i: 0 if i is None else 1, [
            self.zero,
            self.i,
            self.ii,
            self.iii,
            self.iv,
            self.v,
            self.vi,
            self.vii,
            self.viii,
            self.ix,
            self.x,
            self.xi,
            self.xii,
            self.xiii,
            self.xiv,
            self.xv,
            self.xvi,
            self.xvii,
            self.xviii,
            self.xix,
            self.xx,
            self.xxi,
        ]))

    def json(self):
        return {
            "completed": self.total(),
            "trionfi": {trionfo.variable: trionfo.json_user(self) for trionfo in trionfilist}
        }
