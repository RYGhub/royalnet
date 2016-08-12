import asyncio
import discord
import json
import overwatch
d_client = discord.Client()

# Get player database from the db.json file
file = open("db.json")
db = json.load(file)
file.close()


# When the discord client is ready, print something
@d_client.event
async def on_ready():
    print("Connessione riuscita!")
    print(d_client.user.name)
    print(d_client.user.id)


# Get the discord bot token from "discordtoken.txt"
f = open("discordtoken.txt", "r")
token = f.read()
f.close()

# Start discord bot client but ignore events
d_client.start(token)

# List overwatch players
ow_players = list()
for player in db:
    if db[player]["overwatch"] is not None:
        ow_players.append(db[player]["overwatch"])

