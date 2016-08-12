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

# Start discord bot client but ignore events
async def discord_connect():
    await d_client.login(token)
    print("Discord login was successful!")
    d_client.connect()  # Something's not right here...
    print("Discord connection was successful!")

# List overwatch players
ow_players = list()
for player in db:
    if db[player]["overwatch"] is not None:
        ow_players.append(db[player]["overwatch"])

# Connect to Discord
loop.run_until_complete(discord_connect())
