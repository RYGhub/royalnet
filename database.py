import datetime
import sqlalchemy.exc
import discord
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
    parent_id = Column(Integer, ForeignKey("account.id"))

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


    async def update_data(self):
        # Copy the old stats
        soloq_tier = self.soloq_tier
        soloq_division = self.soloq_division
        flexq_tier = self.flexq_tier
        flexq_division = self.flexq_division
        ttq_tier = self.ttq_tier
        ttq_division = self.ttq_division
        # Get and apply the new data
        try:
            soloq, flexq, ttq = await lol.get_rank_data("euw", self.id)
        except lol.LoLAPIError as e:
            # LoL returns 404 if the account is unranked
            if e.status_code == 404:
                self.soloq_tier = None
                self.soloq_division = None
                self.flexq_tier = None
                self.flexq_division = None
                self.ttq_tier = None
                self.ttq_division = None
        else:
            # Update the user data
            if soloq is not None:
                self.soloq_tier = lol.tiers.index(soloq["tier"])
                self.soloq_division = lol.divisions.index(soloq["entries"][0]["division"])
            else:
                self.soloq_tier = None
                self.soloq_division = None
            if flexq is not None:
                self.flexq_tier = lol.tiers.index(flexq["tier"])
                self.flexq_division = lol.divisions.index(flexq["entries"][0]["division"])
            else:
                self.flexq_tier = None
                self.flexq_division = None
            if ttq is not None:
                self.ttq_tier = lol.tiers.index(ttq["tier"])
                self.ttq_division = lol.divisions.index(ttq["entries"][0]["division"])
            else:
                self.ttq_tier = None
                self.ttq_division = None
        # Mark the user as updated
        self.last_updated = datetime.datetime.now()
        # Return if any stat has changed
        return (soloq_tier != self.soloq_tier) or (soloq_division != self.soloq_division) or (flexq_tier != self.flexq_tier) or (flexq_division != self.flexq_division) or (ttq_tier != self.ttq_tier) or (ttq_division != self.ttq_division)


    def generate_discord_embed(self):
        embed = discord.Embed(type="rich")
        # TODO: change the icon
        embed.set_author(name="League of Legends", url="http://euw.leagueoflegends.com/", icon_url="https://cdn.discordapp.com/attachments/152150752523976704/307558194824216578/icon.png")
        embed.add_field(name="Summoner", value=str(self.summoner_name))
        embed.add_field(name="Level", value=str(self.level))
        if self.soloq_tier is not None:
            embed.add_field(name="Solo/duo SR", value=f"{lol.tiers[self.soloq_tier].capitalize()} {lol.divisions[self.soloq_division]}", inline=False)
            embed.set_thumbnail(url=f"https://royal.steffo.me/loltiers/{lol.tiers[self.soloq_tier].lower()}_{lol.divisions[self.soloq_division].lower()}.png")
        if self.flexq_tier is not None:
            embed.add_field(name="Flex SR", value=f"{lol.tiers[self.flexq_tier].capitalize()} {lol.divisions[self.flexq_division]}", inline=False)
        if self.ttq_tier is not None:
            embed.add_field(name="Twisted Treeline", value=f"{lol.tiers[self.ttq_tier].capitalize()} {lol.divisions[self.ttq_division]}", inline=False)
        embed.colour = discord.Colour(0x09AEBB)
        return embed


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
