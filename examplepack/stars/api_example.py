from starlette.requests import Request
from starlette.responses import *
from royalnet.constellation import *
from royalnet.utils import *


class ApiExampleStar(PageStar):
    path = "/api/example"

    async def page(self, request: Request) -> JSONResponse:
        return JSONResponse({
            "hello": "world",
        })
