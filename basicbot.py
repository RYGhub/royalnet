import asyncio
loop = asyncio.get_event_loop()
import telegram
import random
import datetime


b = telegram.Bot("lul")


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


b.commands["leggi"] = leggi
b.commands["diario"] = diario
b.commands["help"] = help
b.run()