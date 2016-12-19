import asyncio
import requests
import json
loop = asyncio.get_event_loop()

async def get_latest_match(steamidtre: str):
    steamidtre = steamidtre[1:-1].split(":")[2]
    print("[OpenDota] Getting latest match for: {steamid}".format(steamid=steamidtre))
    r = await loop.run_in_executor(None, requests.get, 'https://api.opendota.com/api/players/{steamidtre}/matches?limit=1'.format(steamidtre=steamidtre))
    if r.status_code == 200:
        pj = r.json()
        return pj[0]
    else:
        raise Exception("OpenDota request error")

def get_hero_name(heroid: int):
    j = open("herolist.json", "r")
    herolist = json.loads(j.read())
    for hero in herolist:
        if hero["id"] == heroid:
            return hero["localized_name"]
    return None