from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr


class Halloween2020:
    __tablename__ = "halloween2020"

    @declared_attr
    def _steamid(self):
        return Column(BigInteger, ForeignKey("steam._steamid"), primary_key=True)

    @declared_attr
    def steam(self):
        return relationship("Steam", backref=backref("halloween2020", uselist=False))

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
            "total": self.total(),
            "tarots": {
                "zero": self.zero.timestamp() if self.zero else None,
                "i": self.i.timestamp() if self.i else None,
                "ii": self.ii.timestamp() if self.ii else None,
                "iii": self.iii.timestamp() if self.iii else None,
                "iv": self.iv.timestamp() if self.iv else None,
                "v": self.v.timestamp() if self.v else None,
                "vi": self.vi.timestamp() if self.vi else None,
                "vii": self.vii.timestamp() if self.vii else None,
                "viii": self.viii.timestamp() if self.viii else None,
                "ix": self.ix.timestamp() if self.ix else None,
                "x": self.x.timestamp() if self.x else None,
                "xi": self.xi.timestamp() if self.xi else None,
                "xii": self.xii.timestamp() if self.xii else None,
                "xiii": self.xiii.timestamp() if self.xiii else None,
                "xiv": self.xiv.timestamp() if self.xiv else None,
                "xv": self.xv.timestamp() if self.xv else None,
                "xvi": self.xvi.timestamp() if self.xvi else None,
                "xvii": self.xvii.timestamp() if self.xvii else None,
                "xviii": self.xviii.timestamp() if self.xviii else None,
                "xix": self.xix.timestamp() if self.xix else None,
                "xx": self.xx.timestamp() if self.xx else None,
                "xxi": self.xxi.timestamp() if self.xxi else None,
            }
        }
