import asyncio
import aiohttp
import royalbotconfig

# https://euw.api.riotgames.com/api/lol/EUW/v1.4/summoner/52348350?api_key=RGAPI-1008c33d-b0a4-4091-8600-27022d570964

class LoLAPIError(Exception):
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text


tiers = ["BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND", "MASTER", "CHALLENGER"]


divisions = ["I", "II", "III", "IV", "V"]


async def get_json(url, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, **kwargs) as response:
            json = await response.json()
            if response.status != 200:
                raise LoLAPIError(response.status, f"Riot API returned {response.status}")
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
        data = await get_json(f"https://{region.lower()}.api.riotgames.com/api/lol/{region.upper()}/v1.4/summoner/{summoner_id}", params=params)
        return data[str(summoner_id)]
    elif summoner_name is not None:
        data = await get_json(f"https://{region.lower()}.api.riotgames.com/api/lol/{region.upper()}/v1.4/summoner/by-name/{summoner_name}", params=params)
        return data[summoner_name.lower().replace(" ", "")]


async def get_rank_data(region: str, summoner_id: int):
    params = {
        "api_key": royalbotconfig.lol_token
    }
    data = await get_json(f"https://{region.lower()}.api.riotgames.com/api/lol/{region.upper()}/v2.5/league/by-summoner/{summoner_id}/entry", params=params)
    soloq = None
    flexq = None
    ttq = None
    for entry in data[str(summoner_id)]:
        if entry["queue"] == "RANKED_SOLO_5x5":
            soloq = entry
        elif entry["queue"] == "RANKED_FLEX_SR":
            flexq = entry
        elif entry["queue"] == "RANKED_FLEX_TT":
            ttq = entry
    return soloq, flexq, ttq