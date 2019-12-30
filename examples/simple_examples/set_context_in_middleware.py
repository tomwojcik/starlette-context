import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from starlette_context import context, BasicContextMiddleware


async def index(request: Request):
    return JSONResponse(context.dict())


routes = [Route("/", index)]

app = Starlette(debug=True, routes=routes)
app.add_middleware(BasicContextMiddleware)
uvicorn.run(app, host="0.0.0.0")
