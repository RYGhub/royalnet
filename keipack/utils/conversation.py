from royalnet.commands import CommandInterface
from .emotion import Emotion


class Conversation:
    def __init__(self, interface: CommandInterface):
        self.generator = self._generator()
        self.interface: CommandInterface = interface

        self._person = None
        self._session = None
        self._message = None

    async def _generator(self):
        yield
        raise NotImplementedError()

    @classmethod
    async def create(cls, interface: CommandInterface):
        conv = cls(interface=interface)
        await conv.generator.asend(None)
        return conv

    async def next(self, session, person, message):
        self._session = session
        self._person = person
        self._message = message
        reply = await self.generator.asend(None)
        return reply


# noinspection PyTupleAssignmentBalance
class ExampleConversation(Conversation):
    async def _generator(self):
        yield
        yield Emotion.HAPPY, "Ciao!"

        response = await self.interface.call_herald_event("discord", "discord_cv")
        yield Emotion.SURPRISED, f"Ci sono {len(response['guild']['members'])} persone in RYG."

        yield Emotion.NEUTRAL, "Questa è una conversazione di prova."
        yield await ExampleConversation.create(self.interface)
        yield Emotion.WORRIED, "Questo non dovrebbe mai venire fuori."
