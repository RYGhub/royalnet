import re
from typing import *
from royalnet.commands import CommandInterface
from royalnet.utils import *
from .emotion import Emotion
from ..tables import KeiPerson, KeiMessage
from ..utils import any_in_string


class Conversation:
    def __init__(self, interface: CommandInterface):
        self.generator = self._generator()
        self.interface: CommandInterface = interface

        self._person: Optional[KeiPerson] = None
        self._message: Optional[KeiMessage] = None
        self._previous: Optional[str] = None
        self._session = None

    async def _generator(self):
        yield
        raise NotImplementedError()

    @classmethod
    async def create(cls, interface: CommandInterface):
        conv = cls(interface=interface)
        await conv.generator.asend(None)
        return conv

    async def next(self, session, person, message, previous):
        self._session = session
        self._person = person
        self._message = message
        self._previous = previous
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
        yield Emotion.NEUTRAL, "Ciao!"
        yield Emotion.QUESTION, "Come sei arrivato qui...?"
        yield Emotion.HAPPY, "Capisco... Ad ogni modo, sono Kei! Tu come ti chiami?"
        yield NameConversation.create(self.interface)


class NameConversation(Conversation):
    async def _generator(self):
        yield

        while True:
            name = self._message.message.strip().strip(".,;:!?").lower()
            name = re.sub(r"\s*mi\s*chiamo\s*", "", name)
            name = re.sub(r"\s*il\s*mio\s*nome\s*[eèé]\s*", "", name)
            name = re.sub(r"\s*sono\s*", "", name)
            name = re.sub(r"\W", "", name)

            if name == "kei":
                yield Emotion.SURPRISED, "Davvero ti chiami come me?\n" \
                                         "Perche' non mi dici un nome diverso?\n" \
                                         "Altrimenti rischiamo di confonderci..."
                continue

            self._person.name = name
            await asyncify(self._session.commit())
            break

        yield Emotion.GRIN, f"O-kei! {self._person.name}!"
        yield Emotion.HAPPY, "Saro' sempre a tua disposizione quando mi vorrai dire qualcosa!"
        yield Emotion.QUESTION, "Pero' prima ti vorrei chiedere un favore..."
        yield Emotion.NEUTRAL, "Qualcuno ha criptato con delle password tutti i miei file...\n" \
                               "Se ne trovi qualcuna in giro, potresti dirmela?\n"

        while True:
            if self._message.message == "no":
                yield Emotion.CRY, "Non farmi questo... Per piacere, accetta!"
            else:
                break

        yield Emotion.HAPPY, "Grazie! Prometto che quando riavro' tutto ti ricompensero' adeguatamente!"


class MainConversation(Conversation):
    async def _generator(self):
        yield

        yield Emotion.HAPPY, "Di cosa vuoi parlare?"

        while True:
            msg = self._message.message

            if any_in_string([r"gatt[oiae]", "ny[ae]+", "mi+a+o+", "me+o+w+", "felin[oi]", "mici[ao]"], msg):
                yield Emotion.CAT, "Nyan!"

            else:
                yield Emotion.QUESTION, "...?"
