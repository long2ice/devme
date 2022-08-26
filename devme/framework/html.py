from typing import Callable, List, Optional

from loguru import logger

from devme.caddy.volumes import VolumeSite
from devme.enums import FrameworkType
from devme.framework import Framework
from devme.schema import Env


class Html(Framework):
    type = FrameworkType.html

    def __init__(
        self,
        project_name: str,
        git_url: str,
        domains: List[str],
        log_callback: Callable = None,
        image: Optional[str] = None,
        envs: Optional[List[Env]] = None,
        root: str = ".",
        ssl: bool = False,
        branch: str = "main",
    ):
        super().__init__(project_name, git_url, log_callback, image, envs, root, ssl, branch)
        self.domains = domains

    def get_cmds(self):
        return [
            f"git clone -b {self.branch} --depth 1 {self.git_url} {self.project_name}",
            f"rm -rf /srv/{self.project_name}",
            f"mv {self.source_dir} /srv/{self.project_name}",
        ]

    async def build(self):
        cmd = " && ".join(self.get_cmds())
        container = await self.docker.containers.run(
            config={
                "Image": self.image,
                "Cmd": ["bash", "-c", cmd],
                "Env": [str(env) for env in self.envs or []],
                "HostConfig": {"AutoRemove": True, "Mounts": [VolumeSite]},
            },
            name=f"devme-{self.project_name}-builder",
        )
        async for item in container.log(stderr=True, stdout=True, follow=True):
            if self.log_callback:
                await self.log_callback(item)
            logger.debug(item)
        logger.success(f"build project {self.project_name} success")

    async def deploy(self):
        return await self.caddy.add_file_server(self.domains)
