import asyncio
import discord

client = discord.Client()


@client.event
async def on_ready():
    print("Connessione riuscita!")
    print(client.user.name)
    print(client.user.id)

client.run("token")
