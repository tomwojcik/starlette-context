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
    # adding some dummy data so it actually has some context
    import datetime
    import uuid

    set_context(
        a="b", ts=str(datetime.datetime.utcnow()), uuid=uuid.uuid4().hex
    )

    return JSONResponse(get_context())


routes = [Route("/", index)]

app = Starlette(debug=True, routes=routes)
app.add_middleware(CreateEmptyContextMiddleware)
uvicorn.run(app, host="0.0.0.0")
