from starlette.requests import Request
from starlette.responses import *
from royalnet.constellation import *
from royalnet.utils import *


class ApiExcsampleStar(ExceptionStar):
    error = 404

    async def page(self, request: Request) -> JSONResponse:
        return JSONResponse({
            "error": "404 not found",
        })
