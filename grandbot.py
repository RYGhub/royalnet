import asyncio
loop = asyncio.get_event_loop()
import telegram
import random
import datetime
import async_timeout
import aiohttp
import royalbotconfig
import json
import database
import markovify
import discord

b = telegram.Bot(royalbotconfig.telegram_token)
d = discord.Client()

def currently_logged_in(update):
    """Trova l'utente connesso all'account di Telegram che ha mandato l'update."""
    session = database.Session()
    user = session.query(database.User).filter_by(telegram_id=update.message.sent_from.user_id).first()
    return user


async def diario(bot, update, arguments):
    """Aggiungi una frase al diario Royal Games.

Devi essere un Royal per poter eseguire questo comando.

Sintassi: `/diario <frase>`"""
    if not currently_logged_in(update).royal:
        await update.message.reply(bot, "⚠ Non sei autorizzato a eseguire questo comando.", parse_mode="Markdown")
        return
    if len(arguments) == 0:
        await update.message.reply(bot, "⚠ Sintassi del comando non valida.\n`/diario <random | markov | numerofrase>`", parse_mode="Markdown")
        return
    entry = " ".join(arguments)
    if not entry.isprintable():
        await update.message.reply(bot, "⚠ La frase che stai provando ad aggiungere contiene caratteri non ASCII, quindi non è stata aggiunta.\nToglili e riprova!", parse_mode="Markdown")
        return
    entry = entry.replace("\n", " ")
    time = update.message.date.timestamp()
    file = open("diario.txt", "a", encoding="utf8")
    file.write(f"{int(time)}|{entry}\n")
    file.close()
    del file
    await update.message.reply(bot, "Aggiunto al diario!", parse_mode="Markdown")


async def leggi(bot, update, arguments):
    """Leggi una frase dal diario Royal Games.

Puoi visualizzare il diario [qui](https://royal.steffo.me/diario.htm), leggere una frase casuale scrivendo `/leggi random` o leggere una frase specifica scrivendo `/leggi <numero>`.

Sintassi: `/leggi <random | numerofrase>`"""
    if len(arguments) == 0 or len(arguments) > 1:
        await update.message.reply(bot, "⚠ Sintassi del comando non valida.\n`/leggi <random | numerofrase>`", parse_mode="Markdown")
        return
    file = open("diario.txt", "r")
    entries = file.read().split("\n")
    file.close()
    if arguments[0] == "random":
        entry_number = random.randrange(len(entries))
    else:
        entry_number = arguments[0]
    entry = entries[entry_number].split("|", 1)
    date = datetime.datetime.fromtimestamp(entry[0]).isoformat()
    text = entry[1]
    await update.message.reply(bot, f"Frase #{entry_number} | {date}\n{text}", parse_mode="Markdown")


async def markov(bot, update, arguments):
    """Genera una frase del diario utilizzando le catene di Markov.

Puoi specificare con che parola deve iniziare la frase generata.

Sintassi: `/markov [inizio]`"""
    file = open("diario.txt", "r", encoding="utf8")
    # Clean the diario
    clean_diario = str()
    # Remove the timestamps in each row
    for row in file:
        clean_diario += row.split("|", 1)[1].lower()
    # The text is split by newlines
    generator = markovify.NewlineText(clean_diario)
    file.close()
    if len(arguments) == 0:
        # Generate a sentence with a random start
        text = generator.make_sentence(tries=50)
    else:
        # Generate a sentence with a specific start
        start = " ".join(arguments)
        try:
            text = generator.make_sentence_with_start(start, tries=100)
        # No entry can start in that word.
        except KeyError:
            await update.message.reply(bot, f"⚠ Non sono state trovate corrispondenze nel diario dell'inizio che hai specificato.", parse_mode="Markdown")
            return
    if text is not None:
        await update.message.reply(bot, f"*Frase generata:*\n{text}", parse_mode="Markdown")
    else:
        await update.message.reply(bot, f"⚠ Il bot non è riuscito a generare una nuova frase.\nSe è la prima volta che vedi questo errore, riprova, altrimenti prova a cambiare configurazione.")


async def help_cmd(bot, update, arguments):
    """Visualizza la descrizione di un comando.

Sintassi: `/help [comando]`"""
    if len(arguments) == 0:
        await update.message.reply(bot, help.__doc__, parse_mode="Markdown")
    elif len(arguments) > 1:
        await update.message.reply(bot, "⚠ Sintassi del comando non valida.\n`/help [comando]`", parse_mode="Markdown")
    else:
        if arguments[0] in b.commands:
            await update.message.reply(bot, b.commands[arguments[0]].__doc__, parse_mode="Markdown")
        else:
            await update.message.reply(bot, "⚠ Il comando specificato non esiste.", parse_mode="Markdown")


async def discord(bot, update, arguments):
    """Manda un messaggio a #chat di Discord.

Sintassi: `/discord <messaggio>`"""
    # TODO: create a discord module
    # Send a message through a Discord webhook
    # Message to send
    if len(arguments) == 0:
        await update.message.reply(bot, "⚠ Sintassi del comando non valida.\n`/discord <messaggio>`", parse_mode="Markdown")
        return
    username = str(update.message.sent_from)
    message = " ".join(arguments)
    # Parameters to send
    params = {
        # TODO: show the message sender's Discord username
        "content": f"{username}: {message}"
    }
    # Headers to send
    headers = {
        "Content-Type": "application/json"
    }
    # Request timeout is 10 seconds.
    with async_timeout.timeout(10):
        # Create a new session for each request.
        async with aiohttp.ClientSession() as session:
            # Send the request to the Discord webhook
            async with session.request("POST", royalbotconfig.discord_webhook, data=json.dumps(params), headers=headers) as response:
                # Check if the request was successful
                if response.status != 204:
                    # Request failed
                    # Answer on Telegram
                    await update.message.reply(bot, "⚠ L'invio del messaggio è fallito. Oops!", parse_mode="Markdown")
                    # TODO: handle Discord webhooks errors
                    raise Exception("Qualcosa è andato storto durante l'invio del messaggio a Discord.")
                # Answer on Telegram
                await update.message.reply(bot, "Richiesta inviata.", parse_mode="Markdown")


async def sync(bot, update, arguments):
    """Connetti il tuo account Telegram al Database Royal Games.

Sintassi: `/sync <username> <password>`"""
    if len(arguments) != 2:
        await update.message.reply(bot, "⚠ Sintassi del comando non valida.\n`/sync <username> <password>`", parse_mode="Markdown")
        return
    # Try to login
    session, logged_user = database.login(arguments[0], arguments[1])
    # Check if the login is successful
    if logged_user is not None:
        # Add the telegram_id to the user if it's missing
        if logged_user.telegram_id is None:
            # Handle duplicate
            logged_user.telegram_id = update.message.sent_from.user_id
            session.commit()
            print(f"{logged_user} ha sincronizzato l'account.")
            await update.message.reply(bot, f"Sincronizzazione riuscita!\nSei loggato come `{logged_user}`.", parse_mode="Markdown")
        else:
            await update.message.reply(bot, "⚠ L'account è già stato sincronizzato.", parse_mode="Markdown")
    else:
        await update.message.reply(bot, "⚠ Username o password non validi.", parse_mode="Markdown")


async def changepassword(bot, update, arguments):
    """Cambia la tua password del Database Royal Games.

Sintassi: `/changepassword <newpassword>`"""
    if len(arguments) != 2:
        await update.message.reply(bot, "⚠ Sintassi del comando non valida.\n`/changepassword <oldpassword> <newpassword>`", parse_mode="Markdown")
        return
    # TODO: this can be improved, maybe?
    logged_user = currently_logged_in(update)
    # Check if the login is successful
    if logged_user is not None:
        # Change the password
        database.change_password(logged_user.username, arguments[1])
        await update.message.reply(bot, f"Il cambio password è riuscito!\n\n_Info per smanettoni: la tua password è hashata nel database come_ `{logged_user.password}`.", parse_mode="Markdown")
    else:
        await update.message.reply(bot, "⚠ Username o password non validi.", parse_mode="Markdown")


async def cv(bot, update, arguments):
    """Visualizza lo stato attuale della chat vocale Discord.

Sintassi: `/cv`"""
    if len(arguments) != 0:
        await update.message.reply(bot, "⚠ Sintassi del comando non valida.\n`/cv`", parse_mode="Markdown")
        return
    # Wait for the Discord bot to login
    while not d.is_logged_in:
        await asyncio.sleep(1)
    # Find all the users in the server
    # Change this if the bot is logged in more than one server at once?
    users = list(d.get_all_members())
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
                status = "🔵"
            elif user.status.name == "dnd":
                status = "⚪"
            elif user.status.name == "idle":
                status = "⚫"
            elif user.status.name == "offline":
                status = "⚪"
            else:
                status = "❓"
            # Voice status
            if user.bot:
                volume = "🎵"
            elif user.voice.deaf or user.voice.self_deaf:
                volume = "🔇"
            elif user.voice.mute or user.voice.self_mute:
                volume = "🔈"
            else:
                volume = "🔊"
            # Game, is formatted
            if user.game is not None:
                game = f"- *{user.game.name}*"
            else:
                game = ""
            # Name
            if user.nick is not None:
                name = user.nick
            else:
                name = user.name
            # Add the user
            to_send += f"{volume} {status} {name} {game}\n"
        # Channel footer
        to_send += "\n"
    await update.message.reply(bot, to_send, parse_mode="Markdown")

if __name__ == "__main__":
    # Init Telegram bot commands
    b.commands["leggi"] = leggi
    b.commands["diario"] = diario
    b.commands["discord"] = discord
    b.commands["sync"] = sync
    b.commands["changepassword"] = changepassword
    b.commands["help"] = help_cmd
    b.commands["markov"] = markov
    b.commands["cv"] = cv
    # Init Telegram bot
    loop.create_task(b.run())
    print("Telegram bot start scheduled!")
    # Init Discord bot
    loop.run_until_complete(d.login(royalbotconfig.discord_token))
    loop.create_task(d.connect())
    print("Discord bot start scheduled!")
    # Run everything!
    loop.run_forever()