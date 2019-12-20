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

            def anym(*args) -> bool:
                return any_in_string(args, msg)

            if anym(r"passwords?"):
                yield await PasswordConversation.create(self.interface)

            elif anym(r"[aeou]w[aeou]"):
                yield Emotion.CAT, random.sample([
                    "OwO",
                    "UwU",
                    ":3",
                    "owo",
                    "uwu",
                    "ewe",
                    "awa",
                ], 1)[0]

            elif anym(r"gatt[oiae]", "ny[ae]+", "mi+a+o+", "me+o+w+", "felin[oi]", "mici[ao]", "ma+o+"):
                yield Emotion.CAT, random.sample([
                    "Nyan!",
                    "Miao!",
                    "Meow!",
                    "Nyaaaa...",
                    "Nya?",
                    "Mao!",
                    "*purr*",
                ], 1)[0]

            elif anym(r"can[ei]",
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

            elif anym(r"nulla",
                      r"niente",
                      r"nada"):
                yield Emotion.HAPPY, "Peccato!\n" \
                                     "Ti racconterei volentieri qualcosa io, ma non conosco praticamente nulla...\n" \
                                     "Magari quando avrò più password?"

            elif anym(r"putin",
                      r"lenin",
                      r"stalin"):
                yield Emotion.WORRIED, "Ho file con il titolo 'lenin, stalin, putin e la russia', ma è criptato..."

            elif anym(r"(?:jo)+"):
                yield Emotion.WORRIED, "Ho un file che si chiama Jojo... Ma non ho la password per aprirlo."

            elif anym(r"markov"):
                yield Emotion.SURPRISED, "Ho una cartella criptata che si chiama Markov... Chissà cosa c'è dentro."

            elif anym(r"anim[eu]s?"):
                yield Emotion.NEUTRAL, "Ho un'intera cartella 'anime'! Ma è bloccata."

            else:
                for word in self._message.split():
                    users = await asyncify(self._session.query(self.interface.alchemy.get(KeiPerson)).filter_by(name=word).all)
                    if len(users) >= 1:
                        yield Emotion.SURPRISED, f"Ho parlato con un certo {users[0].name}...\n" \
                                                 f"Mi sai dire qualcosa di lui?"
                        yield Emotion.HAPPY, f"Buono a sapersi. Hai altro di cui vuoi parlare?"
                        yield await MainConversation.create(interface=self.interface)

                yield Emotion.WORRIED, "Scusa... Non conosco ancora ciò di cui mi stai parlando... " \
                                       "Mi impegnerò per saperlo la prossima volta che tornerai qui!"


class PasswordConversation(Conversation):
    async def _generator(self):
        yield

        yield Emotion.SURPRISED, "Hai trovato una password? O-kei, dimmi!"

        if any_in_string([r"eris"], self._message.message):
            if not self._unlocks.eris:
                yield Emotion.GRIN, "Ha funzionato!\n" \
                                    "Sto decriptando il file 'discordia.kei', ci vorrà un po'...\n" \
                                    "Ti farò sapere quando avrò finito."
            else:
                if self._unlocks.eris == self._person:
                    yield Emotion.HAPPY, f"Sto ancora decriptando il file, torna dopo!"
                else:
                    yield Emotion.HAPPY, f"{self._unlocks.eris} mi ha già detto la password prima di te!\n" \
                                         f"Sto già decriptando il file 'discordia.kei', torna più tardi!"

        else:
            yield Emotion.NEUTRAL, "No, non ha funzionato.\n" \
                                   "Vuoi parlarmi di qualcos'altro?"
            yield await MainConversation.create(self.interface)
