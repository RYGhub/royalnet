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

b = telegram.Bot(royalbotconfig.telegram_token)


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
        await update.message.reply(bot, "⚠ Non sei autorizzato a eseguire questo comando.")
        return
    if len(arguments) == 0:
        await update.message.reply(bot, "⚠ Sintassi del comando non valida.\n`/diario <random | numerofrase>`")
        return
    entry = " ".join(arguments)
    if not entry.isprintable():
        await update.message.reply(bot, "⚠ La frase che stai provando ad aggiungere contiene caratteri non ASCII, quindi non è stata aggiunta.\nToglili e riprova!")
        return
    entry = entry.replace("\n", " ")
    time = update.message.date.timestamp()
    file = open("diario.txt", "a", encoding="utf8")
    file.write(f"{int(time)}|{entry}\n")
    file.close()
    del file
    await update.message.reply(bot, "Aggiunto al diario!")


async def leggi(bot, update, arguments):
    """Leggi una frase dal diario Royal Games.

Puoi visualizzare il diario [qui](https://royal.steffo.me/diario.htm), leggere una frase casuale scrivendo `/leggi random` o leggere una frase specifica scrivendo `/leggi <numero>`.
Puoi anche generare una frase usando catene di markov scrivendo `/leggi markov`.

Sintassi: `/leggi <random | markov | numerofrase>`"""
    if len(arguments) == 0 or len(arguments) > 1:
        await update.message.reply(bot, "⚠ Sintassi del comando non valida.\n`/leggi <random | numerofrase>`")
        return
    file = open("diario.txt", "r", encoding="utf8")
    string = file.read()
    file.close()
    if arguments[0] == "markov":
        generator = markovify.NewlineText(string)
        line = None
        while line is None:
            line = generator.make_sentence()
        entry_number = "???"
    else:
        entries = string.split("\n")
        if arguments[0] == "random":
            entry_number = random.randrange(len(entries))
        else:
            entry_number = arguments[0]
        line = entries[entry_number]
    entry = line.split("|", 1)
    date = datetime.datetime.fromtimestamp(int(entry[0])).isoformat()
    text = entry[1]
    await update.message.reply(bot, f"Frase #{entry_number} | {date}\n{text}")


async def help(bot, update, arguments):
    """Visualizza la descrizione di un comando.

Sintassi: `/help [comando]`"""
    if len(arguments) == 0:
        await update.message.reply(bot, help.__doc__)
    elif len(arguments) > 1:
        await update.message.reply(bot, "⚠ Sintassi del comando non valida.\n`/help [comando]`")
    else:
        if arguments[0] in b.commands:
            await update.message.reply(bot, b.commands[arguments[0]].__doc__)
        else:
            await update.message.reply(bot, "⚠ Il comando specificato non esiste.")


async def discord(bot, update, arguments):
    """Manda un messaggio a #chat di Discord.

Sintassi: `/discord <messaggio>`"""
    # TODO: create a discord module
    # Send a message through a Discord webhook
    # Message to send
    if len(arguments) == 0:
        await update.message.reply(bot, "⚠ Sintassi del comando non valida.\n`/discord <messaggio>`")
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
                    await update.message.reply(bot, "⚠ L'invio del messaggio è fallito. Oops!")
                    # TODO: handle Discord webhooks errors
                    raise Exception("Qualcosa è andato storto durante l'invio del messaggio a Discord.")
                # Answer on Telegram
                await update.message.reply(bot, "Richiesta inviata.")


async def sync(bot, update, arguments):
    """Connetti il tuo account Telegram al Database Royal Games.

Sintassi: `/sync <username> <password>`"""
    if len(arguments) != 2:
        await update.message.reply(bot, "⚠ Sintassi del comando non valida.\n`/sync <username> <password>`")
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
            await update.message.reply(bot, f"Sincronizzazione riuscita!\nSei loggato come `{logged_user}`.")
        else:
            await update.message.reply(bot, "⚠ L'account è già stato sincronizzato.")
    else:
        await update.message.reply(bot, "⚠ Username o password non validi.")


async def changepassword(bot, update, arguments):
    """Cambia la tua password del Database Royal Games.

Sintassi: `/changepassword <newpassword>`"""
    if len(arguments) != 2:
        await update.message.reply(bot, "⚠ Sintassi del comando non valida.\n`/changepassword <oldpassword> <newpassword>`")
        return
    # TODO: this can be improved, maybe?
    logged_user = currently_logged_in(update)
    # Check if the login is successful
    if logged_user is not None:
        # Change the password
        database.change_password(logged_user.username, arguments[1])
        await update.message.reply(bot, f"Il cambio password è riuscito!\n\n_Info per smanettoni: la tua password è hashata nel database come_ `{logged_user.password}`.")
    else:
        await update.message.reply(bot, "⚠ Username o password non validi.")


if __name__ == "__main__":
    b.commands["leggi"] = leggi
    b.commands["diario"] = diario
    b.commands["discord"] = discord
    b.commands["sync"] = sync
    b.commands["changepassword"] = changepassword
    b.commands["help"] = help
    print("Bot started!")
    b.run()