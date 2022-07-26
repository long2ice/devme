from fastapi import APIRouter

from devme.routes.deploy import router as deploy
from devme.routes.project import router as project

router = APIRouter()
router.include_router(project, prefix="/project", tags=["Project"])
router.include_router(deploy, prefix="/deploy", tags=["Deploy"])
