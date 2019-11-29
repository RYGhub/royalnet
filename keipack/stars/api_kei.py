import random
import datetime
from typing import *
from starlette.requests import Request
from starlette.responses import *
from royalnet.constellation import *
from royalnet.utils import *
from ..tables import *
from ..utils import Emotion


class ApiKei(PageStar):
    path = "/api/kei"

    methods = ["POST"]

    async def _generate(self, person, form, session) -> Tuple[Emotion, str]:
        return Emotion.HAPPY, f'Prova'

    async def page(self, request: Request) -> JSONResponse:
        async with self.session_acm() as session:
            form = await request.form()
            person = session.query(self.alchemy.get(KeiPerson)).filter_by(kpid=form["kpid"]).one_or_none()
            if person is None:
                person = self.alchemy.get(KeiPerson)(kpid=form["kpid"])
                session.add(person)
            message = self.alchemy.get(KeiMessage)(kei_person=person, message=form["message"])
            session.add(message)
            await asyncify(session.commit)
            try:
                emotion, text = await self._generate(person, form, session)
            except Exception as e:
                print(e)
                emotion, text = Emotion.NEUTRAL, "...?"
        return JSONResponse({
            "emotion": str(emotion),
            "text": text,
        })
