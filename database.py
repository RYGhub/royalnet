import datetime
import sqlalchemy.exc
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import lol


class NoUsersMatchingError(Exception):
    pass


class InvalidPasswordError(Exception):
    pass


# Initialize the database
engine = create_engine("sqlite:///db.sqlite")
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Diario(Base):
    __tablename__ = "diario"

    id = Column(Integer, primary_key=True)

    text = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<Diario {self.date} {self.text}>"


class Account(Base):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True)

    lol = relationship("LoL")


class LoL(Base):
    __tablename__ = "lol"

    id = Column(Integer, primary_key=True)
    parentid = Column(Integer, ForeignKey("account.id"))

    last_updated = Column(DateTime)
    summoner_name = Column(String, nullable=False)
    level = Column(Integer)
    soloq_division = Column(Integer)
    soloq_tier = Column(Integer)
    flexq_division = Column(Integer)
    flexq_tier = Column(Integer)
    ttq_division = Column(Integer)
    ttq_tier = Column(Integer)

    def __repr__(self):
        return f"<LoL {self.id} {self.summoner_name}>"


Base.metadata.create_all(engine)


def migrate_diario():
    import datetime
    session = Session()
    file = open("diario.txt", encoding="utf8")
    for row in file:
        entry = row.split("|", 1)
        new = Diario()
        new.date = datetime.datetime.fromtimestamp(int(entry[0]))
        new.text = entry[1]
        session.add(new)
    session.commit()


def new_diario_entry(dt, text):
    # Create a new session
    session = Session()
    # Create a new diario entry
    entry = Diario()
    entry.date = dt
    entry.text = text
    # Add the entry to the database
    session.add(entry)
    # Commit the change
    session.commit()


# TODO: improve this
async def update_lol(lid):
    # Create a new database session
    session = Session()
    # Find the user
    user = session.query(Account).join(LoL).filter_by(id=lid).first()
    # Poll the League API for more information
    data = await lol.get_summoner_data("euw", summoner_id=user.lol.id)
    # Update the user data
    user.lol.summoner_name = data["name"]
    user.lol.level = data["level"]
    # Poll the League API for ranked data
    soloq, flexq, ttq = await lol.get_rank_data("euw", lid)
    # Update the user data
    if soloq is not None:
        user.lol.soloq_tier = lol.tiers[soloq["tier"]]
        user.lol.soloq_division = lol.divisions[soloq["entries"][0]["division"]]
    else:
        user.lol.soloq_tier = None
        user.lol.soloq_division = None
    if flexq is not None:
        user.lol.flexq_tier = lol.tiers[flexq["tier"]]
        user.lol.flexq_division = lol.divisions[flexq["entries"][0]["division"]]
    else:
        user.lol.flexq_tier = None
        user.lol.flexq_division = None
    if ttq is not None:
        user.lol.ttq_tier = lol.tiers[ttq["tier"]]
        user.lol.ttq_division = lol.divisions[ttq["entries"][0]["division"]]
    else:
        user.lol.ttq_tier = None
        user.lol.ttq_division = None
    # Mark the user as updated
    user.lol.last_updated = datetime.datetime.now()
    # Commit the changes
    session.commit()