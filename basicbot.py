import asyncio
loop = asyncio.get_event_loop()
import telegram

b = telegram.Bot("hidden")

async def diario(bot, update, arguments):
    # Sì, ho copiato la funzione dal bot vecchio
    if len(arguments) > 0:
        entry = " ".join(arguments)
        if entry.isprintable():
            entry = entry.replace("\n", " ")
            time = update.message.date.timestamp()
            # TODO: add better file handling
            fdiario = open("diario.txt", "a")
            fdiario.write(f"{int(time)}|{entry}\n")
            fdiario.close()
            del fdiario
            await update.message.chat.send_message(bot, "Aggiunto al diario!")

b.commands["diario"] = diario
b.run()