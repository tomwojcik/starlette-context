from fastapi import FastAPI

from context.metadata import PreserveRequestMetadataMiddleware

app = FastAPI(title="PreserveMetadataExample")

from .api import router

app.add_middleware(PreserveRequestMetadataMiddleware)

app.include_router(router)
