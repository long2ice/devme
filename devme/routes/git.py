from typing import List

from fastapi import APIRouter
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from devme.enums import GitType
from devme.models import GitProvider
from devme.schema import Repo
from devme.utils import get_git

router = APIRouter()


@router.get("/{git_id}/repo", response_model=List[Repo])
async def get_git_repos(git_id: int):
    git_provider = await GitProvider.get(pk=git_id)
    git = get_git(git_provider.type)(token=git_provider.token)
    return await git.get_repos()


class CreateGitProvider(BaseModel):
    name: str
    type: GitType
    token: str


@router.post("", response_model=pydantic_model_creator(GitProvider))
async def create_git_provider(req: CreateGitProvider):
    return await GitProvider.create(**req.dict())


@router.post("/repo/import")
async def import_repo():
    pass
