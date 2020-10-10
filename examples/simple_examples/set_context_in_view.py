import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse

from starlette_context import context
from starlette_context.middleware import ContextMiddleware

app = Starlette(debug=True)
app.add_middleware(ContextMiddleware)


@app.route("/")
async def index(request: Request):
    # adding some dummy data so it actually has some context
    import datetime
    import uuid

    context.update(
        a="b", ts=str(datetime.datetime.utcnow()), uuid=uuid.uuid4().hex
    )

    return JSONResponse(context.data)


uvicorn.run(app, host="0.0.0.0")
