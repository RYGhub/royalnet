import asyncio
import discord
client = discord.Client()


# When the discord client is ready, print something
@client.event
async def on_ready():
    print("Connessione riuscita!")
    print(client.user.name)
    print(client.user.id)

# Get the discord bot token from "discordtoken.txt"
f = open("discordtoken.txt", "r")
token = f.read()
f.close()

# Start discord bot client but ignore events
client.start(token)
