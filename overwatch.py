import asyncio
import aiohttp
import json

# Get player database from the db.json file
db = json.load("db.json")

# List overwatch players
players = list()
for player in db:
    if player["overwatch"] is not None:
        players.append(player["overwatch"])