from fastapi import FastAPI

from .middleware import AdditionalUpdateForGiggles, SetRequestAndCorrelationIdInContext

app = FastAPI(title="ExampleLogWithJson")

from .api import router

# order of middlewares is important
app.add_middleware(AdditionalUpdateForGiggles)
app.add_middleware(SetRequestAndCorrelationIdInContext)

app.include_router(router)
