import random
import datetime
from typing import *
from starlette.requests import Request
from starlette.responses import *
from royalnet.constellation import *
from royalnet.utils import *


class ApiKei(PageStar):
    path = "/api/kei"

    async def _generate(self, request, session) -> Tuple[str, str]:
        if request.query_params.get("first", "false") == "true":
            return random.sample([
                ("happy", "Ciao!"),
                ("question", "Come va?"),
                ("happy", "Sono al tuo servizio!"),
                ("happy", "Attendo ordini!"),
                ("cat", "Mandami un messaggio :3"),
            ], 1)[0]
        return "x", "MISSINGNO."

    async def page(self, request: Request) -> JSONResponse:
        async with self.session_acm() as session:
            emotion, text = await self._generate(request, session)
        return JSONResponse({
            "emotion": emotion,
            "text": text,
        })
