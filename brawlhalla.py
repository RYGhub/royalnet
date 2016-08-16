import asyncio
import requests
import bs4
loop = asyncio.get_event_loop()

# Get ladder page for a player
async def get_leaderboard_for(name: str):
    print("[Brawlhalla] Getting leaderboards page for {name}".format(name=name))
    # Get leaderboards page for that name
    r = loop.run_in_executor(None, requests.get, "http://www.brawlhalla.com/rankings/1v1/eu/?p={name}".format(name))
    # Check if the request is successful
    if r.status_code == 200:
        return r
    else:
        raise Exception("Something went wrong in the Brawlhalla request.")
