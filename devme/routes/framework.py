from typing import List

from fastapi import APIRouter

from devme.responses import FrameworkInfo
from devme.utils import framework_map

router = APIRouter()


@router.get("", response_model=List[FrameworkInfo])
async def get_framework():
    ret = []
    for t, f in framework_map.items():
        ret.append({"type": t, "image": f.image})
    return ret
