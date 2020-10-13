from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr
import steam.steamid


class Steam:
    __tablename__ = "steam"

    @declared_attr
    def user_id(self):
        return Column(Integer, ForeignKey("users.uid"))

    @declared_attr
    def user(self):
        return relationship("User", backref=backref("steam"))

    @declared_attr
    def _steamid(self):
        return Column(BigInteger, primary_key=True)

    @property
    def steamid(self):
        return steam.steamid.SteamID(self._steamid)

    @declared_attr
    def persona_name(self):
        return Column(String)

    @declared_attr
    def profile_url(self):
        return Column(String)

    @declared_attr
    def avatar(self):
        return Column(String)

    @declared_attr
    def primary_clan_id(self):
        return Column(BigInteger)

    @declared_attr
    def account_creation_date(self):
        return Column(DateTime)

    @declared_attr
    def account_level(self):
        return Column(Integer, nullable=False, default=0)

    @declared_attr
    def owned_games_count(self):
        return Column(Integer, nullable=False, default=0)

    @declared_attr
    def most_played_game_2weeks(self):
        return Column(Integer, nullable=False, default=753)

    @declared_attr
    def most_played_game_forever(self):
        return Column(Integer, nullable=False, default=753)

    def json(self):
        return {
            "steamid2": self.steamid.as_steam2,
            "steamid3": self.steamid.as_steam3,
            "steamid32": self.steamid.as_32,
            "steamid64": self.steamid.as_64,
            "persona_name": self.persona_name,
            "profile_url": self.profile_url,
            "avatar": self.avatar,
            "primary_clan_id": self.primary_clan_id,
            "account_creation_date": self.account_creation_date.isoformat(),
            "account_level": self.account_level,
            "owned_games_count": self.owned_games_count,
            "most_played_game_2weeks": self.most_played_game_2weeks,
            "most_played_game_forever": self.most_played_game_forever,

            "dota": self.dota.json() if self.dota is not None else None,
            "brawlhalla": self.brawlhalla.json() if self.brawlhalla is not None else None,
            "trionfistatus": self.trionfistatus.json() if (self.trionfistatus is not None and self.trionfistatus.zero
                                                           is not None and self._steamid != 76561198034314260) else None,
        }

    def __repr__(self):
        return f"<Steam account {self._steamid} of {self.user}>"

    def __str__(self):
        return f"[c]steam:{self._steamid}[/c]"
