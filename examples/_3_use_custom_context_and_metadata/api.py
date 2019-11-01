from fastapi import APIRouter

from context.custom.middleware import get_context
from context.metadata.middleware import get_raw_metadata

router = APIRouter()


@router.get("/")
async def index():
    metadata = get_raw_metadata()
    context = get_context()
    return {**metadata, **context}
