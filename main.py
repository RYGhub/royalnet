import asyncio
import discord

client = discord.Client()


@client.event
async def on_ready():
    print("Connessione riuscita!")
    print(client.user.name)
    print(client.user.id)

# Get the discord bot token from "discordtoken.txt"
f = open("discordtoken.txt", "r")
token = f.read()
f.close()

client.run(token)
