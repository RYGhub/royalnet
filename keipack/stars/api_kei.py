from starlette.requests import Request
from starlette.responses import *
from royalnet.web import *
from royalnet.utils import *
import royalnet.packs.common.tables as cpt
import royalpack.tables as rpt


class ApiKei(PageStar):
    path = "/api/kei"

    tables = {}

    async def _generate(self, request: Request, session) -> typing.Tuple[str, str]:
        return "happy", "Ciao!"

    async def page(self, request: Request) -> JSONResponse:
        async with self.session_acm() as session:
            emotion, text = await self._generate(request, session)
        return JSONResponse({
            "emotion": emotion,
            "text": text,
        })
