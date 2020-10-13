from typing import *
import royalnet
import royalnet.commands as rc
import royalnet.utils as ru
import random
import datetime


class FortuneCommand(rc.Command):
    name: str = "fortune"

    description: str = "Quanto sarai fortunato oggi?"

    syntax: str = ""

    _fortunes = [
        "😄 Oggi sarà una fantastica giornata!",
        "😌 Oggi sarà una giornata molto chill e rilassante.",
        "💰 Oggi sui tuoi alberi cresceranno più Stelline!",
        "🍎 Oggi un unicorno ti lascerà la sua Blessed Apple!",
        "📈 Oggi il tuo team in ranked sarà più amichevole e competente del solito!",
        "🏝 Oggi potrai raggiungere l'Isola Miraggio!",
        "🐱 Oggi vedrai più gatti del solito su Internet!",
        "🐶 Oggi vedrai più cani del solito su Internet!",
        "🐦 Oggi vedrai più uccelli del solito su Internet!",
        "🔥 Oggi vedrai più flame del solito su Internet!",
        "🤬 Oggi vedrai più discorsi politici del solito su Internet!",
        "🐌 Oggi incontrerai una chiocciola sperduta!",
        "🎁 Oggi i dispenser di regali in centro funzioneranno senza problemi!",
        "🥕 Oggi il tuo raccolto avrà qualità Iridium Star!",
        "🔴 Oggi troverai più oggetti di rarità rossa del solito!",
        "✨ Oggi farai molti più multicast!",
        "♦️ Oggi troverai una Leggendaria Dorata!",
        "⭐️ Oggi la stella della RYG ti sembrerà un pochino più dritta!",
        "⭐️ Oggi la stella della RYG ti sembrerà anche più storta del solito!",
        "💎 Oggi i tuoi avversari non riusciranno a deflettere i tuoi Emerald Splash!",
        "⬅️ Oggi le tue supercazzole prematureranno un po' più a sinistra!",
        "➡️ Oggi le tue supercazzole prematureranno un po' più a destra!",
        "🌅 Oggi sarà il giorno dopo ieri e il giorno prima di domani!",
        "🤖 Oggi il Royal Bot ti dirà qualcosa di molto utile!",
        "💤 Oggi rischierai di addormentarti più volte!",
        "🥪 Oggi ti verrà fame fuori orario!",
        "😓 Oggi dirai molte stupidaggini!",
        "🏠 Oggi qualcuno si autoinviterà a casa tua!",
        "📵 Oggi passerai una bella giornata tranquilla senza che nessuno ti chiami!",
        "🎶 Oggi scoprirai un vero [url=https://www.urbandictionary.com/define.php?term=banger]banger[/url]!",
        "🕸 Oggi cadrai trappola di una ragnatela! [i]O ti arriverà in faccia.[/i]",
        "🧻 Oggi fai attenzione alla carta igienica: potrebbe finire!",
        "🔮 Oggi chiederai a @royalgamesbot di dirti la tua /fortune!",
        "🧨 Oggi calpesterai delle [url=https://www.youtube.com/watch?v=Zyef3NU3wqk&t=57]mine di Techies[/url]!",
        "👽 Oggi incontrerai gli UFI!!!1!!uno!",
        "🦾 Oggi uno scienziato pazzo ti proporrà di sostituire il tuo braccio con un braccio-razzo meccanico!",
        "🕵️ Oggi una spia in incognito ti chiederà se hai mai visto the Emoji Movie!",
        "🍕 Oggi mangerai una margherita doppio pomodoro!",
        "🍰 Oggi mangerai una [url=https://www.youtube.com/watch?v=2EWWL3niBWY]torta al gusto di torta[/url]!",
        "🥇 Oggi vincerai qualcosa!",
        "🏴‍☠️ Oggi salperai i sette mari con la tua ciurma pirata!",
        "🕒 Oggi sarà ieri, e domani sarà oggi!",
        "🔙 Oggi torneai indietro nel tempo!",
        "🚨 Oggi suonerà l'allarme della Velvet Room!",
        "♾ Oggi ti sembrerà infinito!",
        "👹 Oggi perfino i demoni avranno paura di te!",
        "🥐 Oggi mangerai una brioche (o lancerai un boomerang)!",
    ]

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        async with data.session_acm() as session:
            author = await data.find_author(session=session, required=True)
            if author.trionfistatus and author.trionfistatus.zero:
                author.trionfistatus.x = datetime.datetime.now()

            today = datetime.date.today()

            h = author.uid * hash(today)

            r = random.Random(x=h)

            message = r.sample(self._fortunes, 1)[0]
            await data.reply(message)
