from fastapi import APIRouter

from devme.routes import deploy, git, project, domain

router = APIRouter()
router.include_router(project.router, prefix="/project", tags=["Project"])
router.include_router(git.router, prefix="/git", tags=["Git"])
router.include_router(deploy.router, prefix="/project/{project_id}/deploy", tags=["Deploy"])
router.include_router(domain.router, prefix="/project/{project_id}/domain", tags=["Domain"])
