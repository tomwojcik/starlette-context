from fastapi import FastAPI

from examples._1_store_request_and_correlation_id_in_context.middleware import (
    PreserveIdentifiersMiddleware,
)

app = FastAPI(title="PreserveIdentifiersExample")

from .api import router

app.add_middleware(PreserveIdentifiersMiddleware)

app.include_router(router)
