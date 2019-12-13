import random
import datetime
import logging
from typing import *
from starlette.requests import Request
from starlette.responses import *
from royalnet.constellation import *
from royalnet.utils import *
from royalnet.commands import CommandInterface
from ..tables import *
from ..utils import *


log = logging.getLogger(__name__)


class ApiKei(PageStar):
    path = "/api/kei"

    methods = ["POST"]

    def __init__(self, interface: CommandInterface):
        super().__init__(interface)
        self._conversations: Dict[str, Conversation] = {}
        log.debug("Kei initialized.")

    async def page(self, request: Request) -> JSONResponse:
        async with self.session_acm() as session:
            form = await request.form()

            kpid = form["kpid"]
            convid = form["convid"]
            msg = form.get("message")
            previous = form.get("previous")

            person = await asyncify(session.query(self.alchemy.get(KeiPerson)).filter_by(kpid=kpid).one_or_none)
            if person is None:
                person = self.alchemy.get(KeiPerson)(kpid=kpid)
                session.add(person)
                first = True
            else:
                first = False
            message = self.alchemy.get(KeiMessage)(kei_person=person, message=msg, previous=previous)
            session.add(message)
            await asyncify(session.commit)
            # Find conversation
            while True:
                if convid not in self._conversations:
                    # Create a new conversation
                    if first:
                        self._conversations[convid] = await FirstConversation.create(self.interface)
                    else:
                        self._conversations[convid] = await StartConversation.create(self.interface)
                    log.info(f"[{convid}] SYSTEM: New conversation created - {self._conversations[convid]}")
                conv: Conversation = self._conversations[convid]

                try:
                    log.info(f"[{convid}] {person}: '{message.message}'")
                except Exception:
                    pass
                try:
                    result = await conv.next(session=session,
                                             person=person,
                                             message=message,
                                             previous=previous)
                except StopAsyncIteration:
                    del self._conversations[convid]
                    continue
                except Exception as e:
                    log.error(f"[{convid}] ERROR: {e}")
                    emotion, text = Emotion.QUESTION, "...?"
                    del self._conversations[convid]
                    break
                else:
                    if isinstance(result, Conversation):
                        self._conversations[convid] = result
                        log.info(f"[{convid}] SYSTEM: Switched conversation - {self._conversations[convid]}")
                    else:
                        emotion, text = result
                        break
        log.info(f"[{convid}] Kei ({emotion.value}): '{text}'")
        return JSONResponse({
            "emotion": str(emotion),
            "text": text,
        }, headers={
            "Access-Control-Allow-Origin": "https://kei.steffo.eu",
        })
