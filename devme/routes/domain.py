from fastapi import APIRouter
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from devme.models import Domain, Project

router = APIRouter()


class ProjectDomain(BaseModel):
    branch: str = "main"
    domain: str


@router.post("", response_model=pydantic_model_creator(Domain))
async def add_project_domain(project_id: int, req: ProjectDomain):
    project = await Project.get(pk=project_id)
    return await Domain.create(project=project, **req.dict())


@router.delete("/{domain_id}")
async def delete_project_domain(project_id: int, domain_id: int):
    project = await Project.get(pk=project_id)
    return await Domain.filter(project=project, id=domain_id).delete()


@router.patch("/{domain_id}", response_model=pydantic_model_creator(Domain))
async def update_project_domain(project_id: int, domain_id: int, req: ProjectDomain):
    project = await Project.get(pk=project_id)
    d = await Domain.get(pk=domain_id, project=project)
    await d.update_from_dict(req.dict()).save()
    return d
