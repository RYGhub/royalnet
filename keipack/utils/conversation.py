import re
import random
from typing import *
from royalnet.commands import CommandInterface
from royalnet.utils import *
from .emotion import Emotion
from ..tables import KeiPerson, KeiMessage, KeiUnlocks
from ..utils.anyinstring import any_in_string


class Conversation:
    def __init__(self, interface: CommandInterface):
        self.generator = self._generator()
        self.interface: CommandInterface = interface

        self._person: Optional[KeiPerson] = None
        self._message: Optional[KeiMessage] = None
        self._previous: Optional[str] = None
        self._session = None
        self._unlocks: Optional[KeiUnlocks] = None

    async def _generator(self):
        yield
        raise NotImplementedError()

    @classmethod
    async def create(cls, interface: CommandInterface):
        conv = cls(interface=interface)
        await conv.generator.asend(None)
        return conv

    async def next(self, session, person, message, previous, unlocks):
        self._session = session
        self._person = person
        self._message = message
        self._previous = previous
        self._unlocks = unlocks
        reply = await self.generator.asend(None)
        return reply

    def anym(self, *args) -> bool:
        return any_in_string(args, self._message.message)


# noinspection PyTupleAssignmentBalance
class ExampleConversation(Conversation):
    async def _generator(self):
        yield

        response = await self.interface.call_herald_event("discord", "discord_cv")
        yield Emotion.SURPRISED, f"Ci sono {len(response['guild']['members'])} persone in RYG."

        yield Emotion.NEUTRAL, "Questa è una conversazione di prova."
        yield await ExampleConversation.create(self.interface)
        yield Emotion.WORRIED, "Questo non dovrebbe mai venire fuori."


# noinspection PyTupleAssignmentBalance
class RygmovieConversation(Conversation):
    async def _generator(self):
        yield

        yield Emotion.HAPPY, "Ciao! Sono Kei!"
        yield Emotion.HAPPY, "Non ci conosciamo, ma volevo augurarvi comunque buona visione!"
        yield Emotion.WINK, "Chissà, magari prossimamente ci reincontreremo, e avremo la possibilità di parlarci!"
        yield Emotion.HAPPY, "O-kei, ciao!"


# noinspection PyTupleAssignmentBalance
class FirstConversation(Conversation):
    async def _generator(self):
        yield
        yield Emotion.HAPPY, "Ciao!"
        yield Emotion.HAPPY, "Come hai trovato questo posto?"
        yield Emotion.HAPPY, "Capisco... Ad ogni modo, io sono Kei! Tu come ti chiami?"
        yield await NameConversation.create(self.interface)


class NameConversation(Conversation):
    async def _generator(self):
        yield

        while True:
            name = self._message.message.strip().strip(".,;:!?").replace(" ", "").lower()
            name = re.sub(r"\s*mi\s*chiamo\s*", "", name)
            name = re.sub(r"\s*il\s*mio\s*nome\s*[eèé]\s*", "", name)
            name = re.sub(r"\s*sono\s*", "", name)
            name = re.sub(r"\W", "", name)

            if name == "kei":
                yield Emotion.SURPRISED, "Davvero ti chiami come me?\n" \
                                         "Perchè non mi dici un nome diverso?\n" \
                                         "Altrimenti rischiamo di confonderci..."
                continue

            self._person.name = name
            await asyncify(self._session.commit)
            break

        yield Emotion.GRIN, f"O-kei! {self._person.name}!"
        yield Emotion.HAPPY, "Sarò sempre a tua disposizione quando mi vorrai dire qualcosa!"
        yield Emotion.HAPPY, "Però prima ti vorrei chiedere un favore..."
        yield Emotion.NEUTRAL, "Qualcuno ha criptato con delle password tutti i miei file...\n" \
                               "Se ne trovi qualcuna in giro, potresti dirmela?\n"

        while True:
            if self._message.message == "no":
                yield Emotion.CRY, "Non puoi farmi questo... Per piacere, accetta!"
            else:
                break

        yield Emotion.HAPPY, "Grazie! Ti prometto che quando riavrò tutti i miei file ti ricompenserò adeguatamente!"
        yield Emotion.HAPPY, "Di cosa vuoi parlare adesso?"
        yield await MainConversation.create(self.interface)


class StartConversation(Conversation):
    async def _generator(self):
        yield

        yield Emotion.HAPPY, random.sample([
            "Di cosa vuoi parlare?",
            "Parlando con te imparo nuove cose!"
        ], 1)[0]
        yield await MainConversation.create(self.interface)


class MainConversation(Conversation):
    async def _generator(self):
        yield

        while True:
            msg = self._message.message

            if self.anym(r"passwords?"):
                yield await PasswordConversation.create(self.interface)

            elif self.anym(r"kei"):
                yield Emotion.HAPPY, "Kei. Sono io!\n" \
                                     "Sono un'intelligenza artificiale che migliora man mano che le persone le parlano!"

            elif self.anym(r"[aeou]w[aeou]"):
                yield Emotion.CAT, random.sample([
                    "OwO",
                    "UwU",
                    ":3",
                    "owo",
                    "uwu",
                    "ewe",
                    "awa",
                ], 1)[0]

            elif self.anym(r"gatt[oiae]", "ny[ae]+", "mi+a+o+", "me+o+w+", "felin[oi]", "mici[ao]", "ma+o+"):
                yield Emotion.CAT, random.sample([
                    "Nyan!",
                    "Miao!",
                    "Meow!",
                    "Nyaaaa...",
                    "Nya?",
                    "Mao!",
                    "*purr*",
                ], 1)[0]

            elif self.anym(r"can[ei]",
                           r"dog(?:g(?:hi|os?)|s)?",
                           r"corgis?",
                           r"cagnolin[oiae]",
                           r"wo+f+",
                           r"b[ao]+r+k+",
                           r"ba+u+"):
                yield Emotion.CAT, random.sample([
                    "Woof!",
                    "Bark!",
                    "Bork!",
                    "*arf* *arf*",
                ])

            elif self.anym(r"fu[wr][wr]y"):
                yield Emotion.HAPPY, "Sento continuamente parlare di 'furry'...\n" \
                                     "Ma cosa vuol dire? Non so nulla a riguardo..."
                yield Emotion.HAPPY, "...O-kei! Studierò attentamente la tua risposta!"

            elif self.anym(r"nulla",
                           r"niente",
                           r"nada"):
                yield Emotion.HAPPY, "Peccato!\n" \
                                     "Ti racconterei volentieri qualcosa io, ma non conosco praticamente nulla...\n" \
                                     "Magari quando avrò più password?"

            elif self.anym(r"doot\s*doot\s*"):
                yield Emotion.DOOTFLUTE, "DOOT DOOT MAGIC FLUTE!"

            elif self.anym(r"doot"):
                yield Emotion.DOOTTRUMPET, "Doot doot!"

            elif self.anym(r"lenin",
                           r"stalin",
                           r"comunismo",
                           r"communism"):
                yield Emotion.WORRIED, "Leggo in uno dei miei file che il comunismo non sembra una bella cosa...\n" \
                                       "Tu cosa ne pensi?"
                yield Emotion.HAPPY, "Interessante. Studierò la tua risposta!"

            elif self.anym(r"(?:jo)+"):
                yield Emotion.SURPRISED, "Ma cos'è Jojo? Ho tanti file a riguardo, ma sono tutti bloccati...\n" \
                                         "Potresti parlarmene?"
                yield Emotion.HAPPY, "Hmmm... O-kei!"

            elif self.anym(r"markov"):
                yield Emotion.SURPRISED, "Ho una cartella criptata che si chiama Markov... Chissà cosa c'è dentro..."

            elif self.anym(r"anim[eu]s?"):
                yield Emotion.NEUTRAL, "Ho un'intera cartella 'anime'! Ma è bloccata."

            elif self.anym(r"rygmovie"):
                yield Emotion.SURPRISED, "rygmovie? Io non ne so assolutamente nulla."

            elif self.anym(r"unica\s*musa\s*di\s*cui\s*abuso"):
                yield Emotion.SURPRISED, "È forse una canzone quella che stavi cantando?\n" \
                                         "L'ho già sentita da qualche parte..."

            elif self.anym(r"pollo"):
                yield Emotion.HAPPY, "Pollo! Yum! Mi hai fatto venire fame."

            else:
                for word in msg.split():
                    users = await asyncify(self._session.query(self.interface.alchemy.get(KeiPerson)).filter_by(name=word).all)
                    if len(users) >= 1:
                        yield Emotion.SURPRISED, f"Ho parlato con un certo {users[0].name}...\n" \
                                                 f"Mi sai dire qualcosa di lui?"
                        yield Emotion.SMUG, f"Farò buon uso di questa informazione. Hai altro di cui vuoi parlare?"
                        yield await MainConversation.create(interface=self.interface)

                yield Emotion.WORRIED, "Scusa... Non conosco ancora ciò di cui mi stai parlando... " \
                                       "Mi impegnerò per saperlo la prossima volta che tornerai qui!"


class PasswordConversation(Conversation):
    async def _generator(self):
        yield

        yield Emotion.SURPRISED, "Hai trovato una password? O-kei, dimmi!"

        if self.anym(r"eris"):
            if not self._unlocks.eris:
                yield Emotion.GRIN, "O-kei!\n" \
                                    "Sto decriptando il file 'discordia.kei', ci vorrà un po'...\n" \
                                    "Ti farò sapere quando avrò finito."
                self._unlocks.eris = self._person
                await asyncify(self._session.commit)
            else:
                if self._unlocks.eris == self._person:
                    yield Emotion.HAPPY, f"Sto ancora decriptando il file, torna dopo!"
                else:
                    yield Emotion.HAPPY, f"{self._unlocks.eris} mi ha già detto la password prima di te!\n" \
                                         f"Sto già decriptando il file 'discordia.kei', torna più tardi!"

        elif self.anym(r"rygryg"):
            if not self._unlocks.rygryg:
                yield Emotion.GRIN, "O-kei!\n" \
                                    "Funziona!\n" \
                                    "Sto decriptando 'markov.kei', torna più tardi quando avrò finito..."
                self._unlocks.rygryg = self._person
                await asyncify(self._session.commit)
            else:
                if self._unlocks.rygryg == self._person:
                    yield Emotion.HAPPY, f"Sto ancora decriptando il file, torna dopo!"
                else:
                    yield Emotion.HAPPY, f"{self._unlocks.rygryg} mi ha già detto la password prima di te!\n" \
                                         f"Sto già decriptando il file 'markov.kei', torna più tardi!"

        else:
            yield Emotion.NEUTRAL, "No, non ha funzionato.\n" \
                                   "Vuoi parlarmi di qualcos'altro?"
            yield await MainConversation.create(self.interface)
