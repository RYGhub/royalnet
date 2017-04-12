import asyncio
import datetime
import json
import random
import aiohttp
import async_timeout
import extradiscord
import markovify
import database
import royalbotconfig
import telegram

loop = asyncio.get_event_loop()
b = telegram.Bot(royalbotconfig.telegram_token)
d = extradiscord.ExtraClient(royalbotconfig.discord_token)


def currently_logged_in(thing):
    """Trova l'utente connesso all'account di Telegram che ha mandato l'update."""
    # Create a new database session
    session = database.Session()
    # Check if thing is a Telegram update
    if isinstance(thing, telegram.Update):
        user = session.query(database.User).filter_by(telegram_id=thing.message.sent_from.user_id).first()
    # Check if thing is a Discord message
    elif isinstance(thing, extradiscord.discord.Message):
        user = session.query(database.User).filter_by(discord_id=thing.author.id).first()
    # I don't know what thing is.
    else:
        raise TypeError("thing must be either a telegram.Update or a discord.Message")
    return user


async def answer(bot, thing, text):
    """Rispondi al messaggio con il canale corretto."""
    # Answer on Telegram
    if isinstance(thing, telegram.Update):
        await thing.message.reply(bot, text, parse_mode="Markdown")
    # Answer on Discord
    elif isinstance(thing, extradiscord.discord.Message):
        await bot.send_message(thing.channel, text)
    else:
        raise TypeError("thing must be either a telegram.Update or a discord.Message")


async def status_typing(bot, thing):
    """Imposta lo stato a Bot sta scrivendo..."""
    # Set typing status on Telegram
    if isinstance(thing, telegram.Update):
        await thing.message.chat.set_chat_action(bot, "typing")
    # Set typing status on Discord
    elif isinstance(thing, extradiscord.discord.Message):
        await bot.send_typing(thing.channel)
    else:
        raise TypeError("thing must be either a telegram.Update or a discord.Message")


async def display_help(bot, thing, function):
    """Display the help command of a function"""
    # Telegram bot commands start with /
    if isinstance(thing, telegram.Update):
        symbol = "/"
    # Discord bot commands start with !
    elif isinstance(thing, extradiscord.discord.Message):
        symbol = "!"
    # Unknown service
    else:
        raise TypeError("thing must be either a telegram.Update or a discord.Message")
    # Display the help message
    await answer(bot, thing, function.__doc__.format(symbol=symbol))


def find_date(thing):
    """Find the date of a message."""
    if isinstance(thing, telegram.Update):
        date = thing.message.date
    elif isinstance(thing, extradiscord.discord.Message):
        date = thing.timestamp
    else:
        raise TypeError("thing must be either a telegram.Update or a discord.Message")
    return date


async def diario(bot, thing, arguments):
    """Aggiungi una frase al diario Royal Games.

Devi essere un Royal per poter eseguire questo comando.

Sintassi: `{symbol}diario <frase>`"""
    # Set status to typing
    await status_typing(bot, thing)
    # Check the command syntax
    if len(arguments) == 0:
        await display_help(bot, thing, diario)
        return
    # Find the user
    user = currently_logged_in(thing)
    # Prepare the text
    text = " ".join(arguments).strip()
    # Add the new entry
    database.new_diario_entry(find_date(thing), text, user)
    # Answer on Telegram
    await answer(bot, thing, "✅ Aggiunto al diario!")


async def leggi(bot, thing, arguments):
    """Leggi una frase con un id specifico dal diario Royal Games.

Sintassi: {symbol}leggi <numero>"""
    # Set status to typing
    await status_typing(bot, thing)
    # Create a new database session
    session = database.Session()
    # Cast the number to an int
    try:
        n = int(arguments[0])
    except ValueError:
        await answer(bot, thing, "⚠ Il numero specificato non è valido.")
        return
    # Query the diario table for the entry with the specified id
    entry = session.query(database.Diario).filter_by(id=n).first()
    # Check if the entry exists
    if entry is None:
        await answer(bot, thing, "⚠ Non esiste una frase del diario con quel numero.")
        return
    # Display the entry
    await answer(bot, thing, f"*Dal diario Royal Games, il {entry.date}*:\n"
                             f"{entry.text}")


async def helpme(bot, thing, arguments):
    """Visualizza il messaggio di aiuto di un comando.

Sintassi: `/helpme [comando]`"""
    # Set status to typing
    await status_typing(bot, thing)
    # If no command is specified, show the help message for this command.
    if len(arguments) == 0 or len(arguments) > 1:
        await answer(bot, thing, helpme.__doc__)
        return
    # Check the list of telegram commands if the message was sent from Telegram
    if isinstance(thing, telegram.Update):
        if arguments[0] in b.commands:
            await answer(bot, thing, b.commands[arguments[0]].__doc__)
        else:
            await answer(bot, thing, "⚠ Il comando specificato non esiste.")
    # Check the list of discord commands if the message was sent from Discord
    if isinstance(thing, extradiscord.discord.Message):
        if arguments[0] in d.commands:
            await answer(bot, thing, d.commands[arguments[0]].__doc__)
        else:
            await answer(bot, thing, "⚠ Il comando specificato non esiste.")


async def cv(bot, thing, arguments):
    """Visualizza lo stato attuale della chat vocale Discord.

Sintassi: `{symbol}cv`"""
    # Set status to typing
    await status_typing(bot, thing)
    # Check command syntax
    if len(arguments) != 0:
        await answer(bot, thing, cv.__doc__)
        return
    # Wait for the Discord bot to login
    while not d.client.is_logged_in:
        await asyncio.sleep(1)
    # Find all the users in the server
    # Change this if the bot is logged in more than one server at once?
    users = list(d.client.get_all_members())
    # Find all the channels
    channels = dict()
    for user in users:
        if user.voice_channel is not None:
            if user.voice_channel.name not in channels:
                channels[user.voice_channel.name] = list()
            channels[user.voice_channel.name].append(user)
    # Create the string to send to Telegram
    to_send = str()
    for channel in channels:
        # Channel header
        to_send += f"*{channel}:*\n"
        # Users in channel
        for user in channels[channel]:
            # Online status
            if user.status.name == "online":
                # Online
                status = "🔵"
            elif user.status.name == "dnd" or (user.game is not None and user.game.type == 1):
                # Do not disturb or streaming
                status = "🔴"
            elif user.status.name == "idle":
                # Idle
                status = "⚫"
            elif user.status.name == "offline":
                # Invisible
                status = "⚪"
            else:
                # Unknown
                status = "❓"
            # Voice status
            if user.bot:
                # Music bot
                volume = "🎵"
            elif user.voice.deaf or user.voice.self_deaf:
                # Deafened
                volume = "🔇"
            elif user.voice.mute or user.voice.self_mute:
                # Muted
                volume = "🔈"
            else:
                # Speaking
                volume = "🔊"
            # Game, is formatted
            if user.game is not None:
                # Playing
                if user.game.type == 0:
                    # Game name
                    game = f"- *{user.game.name}*"
                # Streaming
                elif user.game.type == 1:
                    # Stream name and url
                    game = f"- [{user.game.name}]({user.game.url})"
            else:
                game = ""
            # Nickname if available, otherwise use the username
            if user.nick is not None:
                name = user.nick
            else:
                name = user.name
            # Add the user
            to_send += f"{volume} {status} {name} {game}\n"
        # Channel footer
        to_send += "\n"
    await answer(bot, thing, to_send)


async def roll(bot, thing, arguments):
    """Lancia un dado a N facce.

Sintassi: `{symbol}roll <max>`"""
    # Set status to typing
    await status_typing(bot, thing)
    # Check the command syntax
    if len(arguments) != 1:
        await answer(bot, thing, "⚠ Sintassi del comando non valida.\n`/roll <max>`",)
        return
    # Roll the dice!
    await answer(bot, thing, f"*Numero generato:* {random.randrange(0, int(arguments[0])) + 1}")


if __name__ == "__main__":
    # Init universal bot commands
    b.commands["diario"] = diario
    d.commands["diario"] = diario
    b.commands["d"] = diario
    b.commands["help"] = helpme
    b.commands["helpme"] = helpme
    d.commands["help"] = helpme
    d.commands["helpme"] = helpme
    b.commands["cv"] = cv
    # Init Telegram bot
    loop.create_task(b.run())
    print("Telegram bot start scheduled!")
    # Init Discord bot
    loop.create_task(d.run())
    print("Discord bot start scheduled!")
    # Run everything!
    loop.run_forever()
