import asyncio
import aiohttp
import royalbotconfig
import enum

# https://euw.api.riotgames.com/api/lol/EUW/v1.4/summoner/52348350?api_key=RGAPI-1008c33d-b0a4-4091-8600-27022d570964

class LoLAPIError(Exception):
    pass


tiers = {
    "BRONZE": 0,
    "SILVER": 1,
    "GOLD": 2,
    "PLATINUM": 3,
    "DIAMOND": 4,
    "MASTER": 5,
    "CHALLENGER": 6
}

divisions = {
    "I": 0,
    "II": 1,
    "III": 2,
    "IV": 3,
    "V": 4
}


async def get_json(url, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, **kwargs) as response:
            json = await session.json()
            if response.status != 200:
                raise LoLAPIError(f"Riot API returned {response.status}")
            return json


async def get_summoner_data(region: str, summoner_id=None, summoner_name=None):
    # Check for the number of arguments
    if bool(summoner_id) == bool(summoner_name):
        # TODO: use the correct exception
        raise Exception("Invalid number of arguments specified")
    params = {
        "api_key": royalbotconfig.lol_token
    }
    if summoner_id is not None:
        data = await get_json(f"https://{region.lower()}.api.riotgames.com/api/lol/{region.upper()}/v1.4/summoner/{summoner_id}")
        return data[summoner_id]
    elif summoner_name is not None:
        data = await get_json(f"https://{region.lower()}.api.riotgames.com/api/lol/{region.upper()}/v1.4/summoner/by-name/{summoner_name}")
        return data[summoner_name]


async def get_rank_data(region: str, summoner_id: int):
    data = await get_json(f"https://{region.lower()}.api.riotgames.com/api/lol/{region.upper()}/v2.5/league/by-summoner/{summoner_id}/entry")
    soloq = None
    flexq = None
    ttq = None
    for entry in data:
        if data["queue"] == "RANKED_SOLO_5x5":
            soloq = entry
        elif data["queue"] == "RANKED_FLEX_SR":
            flexq = entry
        elif data["queue"] == "RANKED_FLEX_TT":
            ttq = entry
    return soloq, flexq, ttq