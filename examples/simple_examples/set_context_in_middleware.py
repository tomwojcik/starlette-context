from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

import uvicorn
from starlette_context import BasicContextMiddleware, context


async def index(request: Request):
    return JSONResponse(context.dict())


routes = [Route("/", index)]

app = Starlette(debug=True, routes=routes)
app.add_middleware(BasicContextMiddleware)
uvicorn.run(app, host="0.0.0.0")
