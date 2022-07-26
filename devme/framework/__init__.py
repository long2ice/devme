import abc
from pathlib import Path
from typing import Callable, List, Optional

import aiodocker

from devme.caddy import ContainerName
from devme.caddy.api import Caddy
from devme.enums import FrameworkType
from devme.schema import Env
from devme.settings import settings


class Framework:
    type: FrameworkType
    image = "node"

    def __init__(
        self,
        project_name: str,
        git_url: str,
        log_callback: Callable = None,
        image: Optional[str] = None,
        envs: Optional[List[Env]] = None,
        root: str = ".",
        ssl: bool = False,
        **kwargs,
    ):
        self.git_url = git_url
        self.project_name = project_name
        self.envs = envs
        self.root = root
        self.source_dir = Path(project_name) / root
        if image:
            self.image = image
        self.docker = aiodocker.Docker(url=settings.docker.host)
        self.log_callback = log_callback
        self.caddy = Caddy(
            project_name=project_name,
            host="127.0.0.1" if settings.caddy.network == "host" else ContainerName,
            port=settings.caddy.api_port,
            ssl=ssl,
        )

    @abc.abstractmethod
    async def build(self):
        pass

    @abc.abstractmethod
    async def deploy(self):
        pass

    @abc.abstractmethod
    def get_cmds(self):
        pass

    async def clear(self):
        await self.docker.close()
        await self.caddy.close()
