import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from starlette_context import (
    EmptyContextMiddleware,
    context
)


async def index(request: Request):
    # adding some dummy data so it actually has some context
    import datetime
    import uuid

    context.update(
        a="b", ts=str(datetime.datetime.utcnow()), uuid=uuid.uuid4().hex
    )

    return JSONResponse(context.dict())


routes = [Route("/", index)]

app = Starlette(debug=True, routes=routes)
app.add_middleware(EmptyContextMiddleware)
uvicorn.run(app, host="0.0.0.0")
