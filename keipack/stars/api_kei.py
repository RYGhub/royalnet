import random
import datetime
from typing import *
from starlette.requests import Request
from starlette.responses import *
from royalnet.constellation import *
from royalnet.utils import *
from ..tables import *
from ..utils import *


class ApiKei(PageStar):
    path = "/api/kei"

    methods = ["POST"]

    def __init__(self, config: Dict[str, Any], constellation: "Constellation"):
        super().__init__(config, constellation)
        self._conversations: Dict[str, Conversation] = {}

    async def page(self, request: Request) -> JSONResponse:
        async with self.session_acm() as session:
            form = await request.form()

            kpid = form["kpid"]
            convid = form["convid"]
            message = form.get("message")
            first = form.get("first", False)

            person = await asyncify(session.query(self.alchemy.get(KeiPerson)).filter_by(kpid=kpid).one_or_none)
            if person is None:
                person = self.alchemy.get(KeiPerson)(kpid=kpid)
                session.add(person)
            message = self.alchemy.get(KeiMessage)(kei_person=person, message=message)
            session.add(message)
            await asyncify(session.commit)
            # Find conversation
            while True:
                if convid not in self._conversations:
                    # Create a new conversation
                    self._conversations[convid] = await ExampleConversation.create()
                conv: Conversation = self._conversations[convid]
                try:
                    emotion, text = await conv.next(session=session, person=person, message=message)
                except StopAsyncIteration:
                    del self._conversations[convid]
                    continue
                except Exception as e:
                    print(e)
                    emotion, text = Emotion.NEUTRAL, "...?"
                else:
                    break
        return JSONResponse({
            "emotion": str(emotion),
            "text": text,
        }, headers={
            "Access-Control-Allow-Origin": "https://kei.steffo.eu",
        })
