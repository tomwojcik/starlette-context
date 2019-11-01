from fastapi import APIRouter

from context.custom import get_context

router = APIRouter()


@router.get("/")
async def index():
    return get_context()
