from .emotion import Emotion

class Conversation:
    def __init__(self):
        self.generator = self._generator()

    async def _generator(self):
        yield
        raise NotImplementedError()

    @classmethod
    async def create(cls):
        conv = cls()
        await conv.generator.asend(None)
        return conv

    async def next(self, session, person, message):
        reply = await self.generator.asend((session, person, message))
        return reply


# noinspection PyTupleAssignmentBalance
class ExampleConversation(Conversation):
    async def _generator(self):
        session, person, message = yield
        session, person, message = yield Emotion.HAPPY, "Ciao!"
        session, person, message = yield Emotion.NEUTRAL, "Questa è una conversazione di prova."
        session, person, message = yield Emotion.X, "X_X"
