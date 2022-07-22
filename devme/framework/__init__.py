import abc
import os.path
from enum import Enum
from pathlib import Path
from typing import List, Optional

import aiodocker

from devme.caddy.api import Caddy
from devme.schema import Env
from devme.settings import settings


class FrameworkType(str, Enum):
    nodejs = "nodejs"
    html = "html"


class Framework:
    type: FrameworkType
    image: str

    def __init__(
        self,
        project_name: str,
        git_url: str,
        image: Optional[str] = None,
        envs: Optional[List[Env]] = None,
        root: str = ".",
    ):
        self.git_url = git_url
        self.project_name = project_name
        self.envs = envs
        self.root = root
        self.source_dir = Path(project_name) / root
        if image:
            self.image = image
        self.docker = aiodocker.Docker(url=settings.docker.host)
        self.caddy = Caddy(port=settings.caddy.api_port)

    @abc.abstractmethod
    async def build(self):
        pass

    @abc.abstractmethod
    async def deploy(self, domains: List[str]):
        pass

    @abc.abstractmethod
    def get_cmds(self):
        pass

    async def clear(self):
        await self.docker.close()
        await self.caddy.close()
