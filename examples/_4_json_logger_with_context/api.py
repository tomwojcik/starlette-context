from fastapi import APIRouter

from context.custom import update_context
from .logger import log

router = APIRouter()


@router.get("/")
async def index():
    log.info("test")
    update_context(yet_another_update="from api now")
    log.info("test2")
    return {"msg": "ok"}
