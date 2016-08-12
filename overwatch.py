import asyncio
import requests
import json
loop = asyncio.get_event_loop()

# Get player database from the db.json file
file = open("db.json")
db = json.load(file)
file.close()

# List overwatch players
players = list()
for player in db:
    if db[player]["overwatch"] is not None:
        players.append(db[player]["overwatch"])

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

loop.run_until_complete(get_player_data("pc", "eu", "SteffoRYG#2876"))
