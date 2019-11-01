from typing import NoReturn

from fastapi import APIRouter

from .logger import log

router = APIRouter()


@router.get("/")
async def index() -> NoReturn:
    log.info("pre exception")
    return 1 / 0
