from typing import List, Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field
from starlette.background import BackgroundTasks
from tortoise.contrib.pydantic import pydantic_model_creator

from devme.enums import DeployStatus, FrameworkType
from devme.models import Deploy, Project, Domain
from devme.utils import get_framework

router = APIRouter()


@router.get("", response_model=List[pydantic_model_creator(Project)])
async def get_projects():
    return await Project.all()


class CreateProject(BaseModel):
    name: str = Field(..., example="gema")
    url: str = Field(..., example="https://github.com/long2ice/gema-web.git")
    framework: FrameworkType = Field(..., example=FrameworkType.nodejs)
    image: Optional[str]
    root: str = "."
    deployment: dict
    env: Optional[dict]
    git_provider_id: Optional[int]


@router.post("", response_model=pydantic_model_creator(Project))
async def create_project(req: CreateProject):
    project = await Project.create(**req.dict(exclude_none=True, exclude_unset=True))
    return project


class UpdateProject(BaseModel):
    name: Optional[str] = Field(None, example="gema")
    url: Optional[str] = Field(None, example="https://github.com/long2ice/gema-web.git")
    framework: Optional[FrameworkType] = Field(None, example=FrameworkType.nodejs)
    image: Optional[str]
    root: Optional[str]
    deployment: Optional[dict]
    env: Optional[dict]


@router.patch("/{project_id}")
async def update_project(project_id: int, req: UpdateProject):
    project = await Project.get(pk=project_id)
    await project.update_from_dict(req.dict(exclude_none=True, exclude_unset=True)).save()
    return project


@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
):
    project = await Project.get(pk=project_id)
    await project.delete()
