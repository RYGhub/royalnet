import asyncio
import discord
import json
import overwatch

loop = asyncio.get_event_loop()
d_client = discord.Client()

# Get player database from the db.json file
file = open("db.json")
db = json.load(file)
file.close()

# Get the discord bot token from "discordtoken.txt"
f = open("discordtoken.txt", "r")
token = f.read()
f.close()

# List overwatch players
ow_players = list()
for player in db:
    if db[player]["overwatch"] is not None:
        ow_players.append(db[player]["overwatch"])

# Every 300 seconds, update player status and check for levelups
async def overwatch_level_up(timeout):
    while True:
        # Update data for every player in list
        for ow_player in ow_players:
            r = await overwatch.get_player_data(**ow_player)
            if r["data"]["level"] > ow_player["level"]:
                await d_client.send_message(d_client.get_channel("213655027842154508"), "Level up!")
                ow_player["level"] = r["data"]["level"]
        # Wait for the timeout
        await asyncio.sleep(timeout)

loop.create_task(overwatch_level_up(30))
d_client.run(token)