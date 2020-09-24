from typing import *
import abc
import aiohttp
import logging
import royalnet.commands as rc

if TYPE_CHECKING:
    from .trionfistatus import TrionfiStatus


log = logging.getLogger(__name__)


__all__ = [
    "Check",
    "NullCheck",
    "CheckPlayedSteamGame",
    "CheckAchievementSteamGame",
]


class Check(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def check(self, status: "TrionfiStatus", key: str) -> bool:
        raise NotImplementedError()

    def __or__(self, other: "Check"):
        return CheckOr(self, other)

    def __and__(self, other):
        return CheckAnd(self, other)


class NullCheck(Check):
    def __repr__(self):
        return f"{self.__class__.__name__}()"

    async def check(self, status: "TrionfiStatus", key: str) -> bool:
        return False


class CheckPlayedSteamGame(Check):
    def __init__(self, appid: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.appid: int = appid

    def __repr__(self):
        return f"{self.__class__.__name__}({self.appid=})"

    async def check(self, status: "TrionfiStatus", key: str) -> bool:
        log.debug(f"{self}")
        async with aiohttp.ClientSession() as ah_session:
            # noinspection PyProtectedMember
            async with ah_session.get("https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/",
                                      params={
                                          "steamid": status._steamid,
                                          "include_appinfo": "true",
                                          "include_played_free_games": "true",
                                          "include_free_sub": "true",
                                          "appids_filter": self.appid,
                                          "key": key,
                                      }) as response:
                try:
                    j = await response.json()
                except Exception as e:
                    log.error(f"{e}")
                    return False

                games = j["response"]["games"]
                for game in games:
                    if game["appid"] != self.appid:
                        continue
                    if game["playtime_forever"] >= 30:
                        return True
                return False


class CheckAchievementSteamGame(Check):
    def __init__(self, appid: int, achievement_name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.appid: int = appid
        self.achivement_name: str = achievement_name

    def __repr__(self):
        return f"{self.__class__.__name__}({self.appid=}, {self.achivement_name=})"

    async def check(self, status: "TrionfiStatus", key: str) -> bool:
        log.debug(f"{self}")
        async with aiohttp.ClientSession() as ah_session:
            # noinspection PyProtectedMember
            async with ah_session.get("http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/",
                                      params={
                                          "steamid": status._steamid,
                                          "appid": self.appid,
                                          "key": key,
                                      }) as response:
                try:
                    j = await response.json()
                except Exception as e:
                    log.error(f"{e}")
                    return False
                if not j["playerstats"]["success"]:
                    log.warning(f"{j}")
                    return False

                achievements = j["playerstats"]["achievements"]
                for ach in achievements:
                    if ach["apiname"] != self.achivement_name:
                        continue
                    return ach["achieved"] == 1
                return False


class CheckOr(Check):
    def __init__(self, first: Check, second: Check, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.first: Check = first
        self.second: Check = second

    def __repr__(self):
        return f"{self.first} or {self.second}"

    async def check(self, status: "TrionfiStatus", key: str) -> bool:
        log.debug(f"{self}")
        return (await self.first.check(status, key)) or (await self.second.check(status, key))


class CheckAnd(Check):
    def __init__(self, first: Check, second: Check, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.first: Check = first
        self.second: Check = second

    def __repr__(self):
        return f"{self.first} and {self.second}"

    async def check(self, status: "TrionfiStatus", key: str) -> bool:
        log.debug(f"{self}")
        return (await self.first.check(status, key)) and (await self.second.check(status, key))
