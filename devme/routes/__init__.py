from fastapi import APIRouter

from devme.routes import deploy, project, git

router = APIRouter()
router.include_router(project.router, prefix="/project", tags=["Project"])
router.include_router(deploy.router, prefix="/deploy", tags=["Deploy"])
router.include_router(git.router, prefix="/git", tags=["Git"])
