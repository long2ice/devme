from typing import List

from fastapi import APIRouter

from devme.enums import FrameworkType

router = APIRouter()


@router.get("", response_model=List[FrameworkType])
async def get_framework():
    return [f for f in FrameworkType]
