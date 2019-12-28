import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from examples.example_with_logger.logger import log
from starlette_context import get_context, PreserveCustomContextMiddleware


async def index(request: Request):
    log.info("Log from view")
    return JSONResponse(get_context())


routes = [Route("/", index)]

app = Starlette(debug=True, routes=routes)
app.add_middleware(PreserveCustomContextMiddleware)
uvicorn.run(app, host="0.0.0.0")
