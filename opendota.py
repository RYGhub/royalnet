import asyncio
import requests
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
