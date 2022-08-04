from typing import List, Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field
from tortoise.contrib.pydantic import pydantic_model_creator

from devme.enums import FrameworkType
from devme.models import GitProvider, Project
from devme.settings import settings
from devme.utils import get_git, get_owner_repo_from_url

router = APIRouter()


@router.get("", response_model=List[pydantic_model_creator(Project)])  # type:ignore
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
    if req.git_provider_id:
        git_provider = await GitProvider.get(pk=req.git_provider_id)
        git = get_git(git_provider.type)(git_provider.token)
        owner, repo = get_owner_repo_from_url(req.url)
        await git.create_webhook(
            owner, repo, settings.site_url + f"/project/{project.pk}/deploy/webhook"
        )
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
    project = await Project.get(pk=project_id).select_related("git_provider")
    if project.git_provider:
        git_provider = project.git_provider
        git = get_git(git_provider.type)(git_provider.token)
        owner, repo = get_owner_repo_from_url(project.url)
        await git.delete_webhook(owner, repo)

    await project.delete()
