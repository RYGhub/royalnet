import asyncio
import json

loop = asyncio.get_event_loop()
import telegram
import random
import datetime
import async_timeout
import aiohttp
import royalbotconfig

b = telegram.Bot(royalbotconfig.telegram_token)


async def diario(bot, update, arguments):
    """Aggiungi una frase al diario Royal Games.

Sintassi: `/diario <frase>`"""
    # Sì, ho copiato la funzione dal bot vecchio
    if len(arguments) == 0:
        await update.message.chat.send_message(bot, "⚠ Sintassi del comando non valida.\n`/diario <random | numerofrase>`")
        return
    entry = " ".join(arguments)
    if not entry.isprintable():
        await update.message.chat.send_message(bot, "⚠ La frase che stai provando ad aggiungere contiene caratteri non ASCII, quindi non è stata aggiunta.\nToglili e riprova!")
        return
    entry = entry.replace("\n", " ")
    time = update.message.date.timestamp()
    # TODO: add better file handling, maybe use GET requests?
    file = open("diario.txt", "a")
    file.write(f"{int(time)}|{entry}\n")
    file.close()
    del file
    await update.message.chat.send_message(bot, "Aggiunto al diario!")


async def leggi(bot, update, arguments):
    """Leggi una frase dal diario Royal Games.

Puoi visualizzare il diario [qui](https://royal.steffo.me/diario.htm), leggere una frase casuale scrivendo `/leggi random` o leggere una frase specifica scrivendo `/leggi <numero>`.

Sintassi: `/leggi <random | numerofrase>`"""
    if len(arguments) == 0 or len(arguments) > 1:
        await update.message.chat.send_message(bot, "⚠ Sintassi del comando non valida.\n`/leggi <random | numerofrase>`")
        return
    # TODO: add better file handling, maybe use GET requests?
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
    await update.message.chat.send_message(bot, f"Frase #{entry_number} | {date}\n{text}")


async def help(bot, update, arguments):
    """Visualizza la descrizione di un comando.

Sintassi: `/help [comando]`"""
    if len(arguments) == 0:
        await update.message.chat.send_message(bot, help.__doc__)
    elif len(arguments) > 1:
        await update.message.chat.send_message(bot, "⚠ Sintassi del comando non valida.\n`/help [comando]`")
    else:
        if arguments[0] in b.commands:
            await update.message.chat.send_message(bot, b.commands[arguments[0]].__doc__)
        else:
            await update.message.chat.send_message(bot, "⚠ Il comando specificato non esiste.")


async def discord(bot, update, arguments):
    """Manda un messaggio a #chat di Discord.

Sintassi: `/discord <messaggio>`"""
    # TODO: create a discord module
    # Send a message through a Discord webhook
    # Message to send
    if len(arguments) == 0:
        await update.message.chat.send_message(bot, "⚠ Sintassi del comando non valida.\n`/discord <messaggio>`")
        return
    username = f"{update.message.sent_from}"
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
                    await update.message.chat.send_message(bot, "⚠ L'invio del messaggio è fallito. Oops!")
                    # TODO: handle Discord webhooks errors
                    raise Exception("Qualcosa è andato storto durante l'invio del messaggio a Discord.")
                # Answer on Telegram
                await update.message.chat.send_message(bot, "Richiesta inviata.")


b.commands["leggi"] = leggi
b.commands["diario"] = diario
b.commands["discord"] = discord
b.commands["help"] = help
b.run()