import asyncio
loop = asyncio.get_event_loop()
import telegram

b = telegram.Bot("ciao pizza")

async def print_message(bot, update):
    print(update.message.content)

b.commands["echo"] = print_message
b.run()