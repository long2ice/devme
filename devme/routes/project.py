from fastapi import APIRouter
from pydantic import BaseModel

from devme.enums import FrameworkType

router = APIRouter()


@router.get("")
async def get_projects():
    pass


class CreateProject(BaseModel):
    name: str
    url: str
    framework: FrameworkType
    image: str
    root: str
    deployment: dict
    env: dict


@router.post("")
async def create_project(req: CreateProject):
    pass


@router.post("/{project_id}/deploy")
async def deploy_project():
    pass
