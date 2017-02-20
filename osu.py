import asyncio
import requests
import functools
loop = asyncio.get_event_loop()

# Load Osu API key from the osutoken.txt file
file = open("osutoken.txt", "r")
token = file.read()
file.close()

async def get_user(user, mode=0):
    print("[Osu!] Getting profile data for {} mode {}".format(user, mode))
    params = {
        "k": token,
        "m": mode,
        "u": user
    }
    # Get the data
    r = await loop.run_in_executor(None, functools.partial(requests.get, timeout=6.1) 'https://osu.ppy.sh/api/get_user?k={k}&m={m}&u={u}'.format(**params))
    if r.status_code == 200:
        return r.json()[0]
    else:
        raise Exception("[Osu!] Unhandled exception during the API request")
