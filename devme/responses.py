from typing import Optional

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from devme.enums import FrameworkType
from devme.models import Project


class FrameworkInfo(BaseModel):
    type: FrameworkType
    image: str


class ProjectInfo(pydantic_model_creator(Project)):
    git_provider_id: Optional[int]
