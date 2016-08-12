import asyncio
import requests
loop = asyncio.get_event_loop()

# Get player data
async def get_player_data(platform: str, region: str, battletag: str):
    # Unofficial API requires - for discriminator numbers
    battletag = battletag.replace("#", "-")
    # GET the json unofficial API response
    r = await loop.run_in_executor(None, requests.get,
                                   'https://api.lootbox.eu/{platform}/{region}/{battletag}/profile'.format(**locals()))
    # Ensure the request is successful
    if r.status_code == 200:
        return r.json()
    elif r.status_code == 404:
        raise Exception("Player not found.")