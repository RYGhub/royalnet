from starlette.requests import Request
from starlette.responses import *
from royalnet.constellation import *
from royalnet.utils import *

# TODO: delete this file!


class ExampleStar(PageStar):
    path = "/example"

    async def page(self, request: Request) -> JSONResponse:
        return HTMLResponse("""<html><body><h1>henlo!</h1></body></html>""")
