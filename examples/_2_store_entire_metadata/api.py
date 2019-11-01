from fastapi import APIRouter

from context.metadata import get_raw_metadata

router = APIRouter()


@router.get("/")
async def index():
    return get_raw_metadata()
