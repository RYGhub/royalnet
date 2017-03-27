import discord
import asyncio
loop = asyncio.get_event_loop()

class ExtraClient:
    def __init__(self, token):
        self.client = discord.Client()
        self.commands = dict()
        self.token = token

        @self.client.event
        async def on_message(message):
            split = message.content.split(" ")
            command = split[0].lstrip("!")
            if command in self.commands:
                await self.commands[command](self.client, message, split[1:])


    async def run(self):
        await self.client.login(self.token)
        await self.client.connect()