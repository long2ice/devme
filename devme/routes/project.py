from fastapi import APIRouter

from devme.framework.html import Html

router = APIRouter()


@router.get("")
async def get_project():
    pass
