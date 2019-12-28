import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from starlette_context import (
    CreateEmptyContextMiddleware,
    get_context,
    set_context,
)


async def index(request: Request):
    set_context(view=True)
    return JSONResponse(get_context())


class ContextFromMiddleware(CreateEmptyContextMiddleware):
    def set_context(self, request: Request) -> dict:
        return {"middleware": True}


routes = [Route("/", index)]

app = Starlette(debug=True, routes=routes)
app.add_middleware(ContextFromMiddleware)
uvicorn.run(app, host='0.0.0.0')
