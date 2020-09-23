from typing import *
import abc
import aiohttp

if TYPE_CHECKING:
    from .trionfistatus import TrionfiStatus


__all__ = [
    "Check",
    "CheckPlayedSteamGame",
    "CheckAchievementSteamGame",
]


class Check(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def check(self, status: "TrionfiStatus") -> bool:
        raise NotImplementedError()

    def __or__(self, other: "Check"):
        return CheckOr(self, other)

    def __and__(self, other):
        return CheckAnd(self, other)


class CheckPlayedSteamGame(Check):
    def __init__(self, appid: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.appid: int = appid

    async def check(self, status: "TrionfiStatus") -> bool:
        async with aiohttp.ClientSession() as ah_session:
            # noinspection PyProtectedMember
            async with ah_session.get("https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/",
                                      params={
                                          "steamid": status._steamid,
                                          "include_appinfo": True,
                                          "include_played_free_games": True,
                                          "include_free_sub": True,
                                          "appids_filter": self.appid,
                                      }) as response:
                try:
                    j = await response.json()
                except Exception:
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

    async def check(self, status: "TrionfiStatus") -> bool:
        async with aiohttp.ClientSession() as ah_session:
            # noinspection PyProtectedMember
            async with ah_session.get("http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/",
                                      params={
                                          "steamid": status._steamid,
                                          "appid": self.appid,
                                      }) as response:
                try:
                    j = await response.json()
                except Exception:
                    return False
                if not j["playerstats"]["success"]:
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

    async def check(self, status: "TrionfiStatus") -> bool:
        return (await self.first.check(status)) or (await self.second.check(status))


class CheckAnd(Check):
    def __init__(self, first: Check, second: Check, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.first: Check = first
        self.second: Check = second

    async def check(self, status: "TrionfiStatus") -> bool:
        return (await self.first.check(status)) and (await self.second.check(status))
