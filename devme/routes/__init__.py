from fastapi import APIRouter
from devme.routes.project import router as project

router = APIRouter()
router.include_router(project, prefix="/project", tags=["Project"])
