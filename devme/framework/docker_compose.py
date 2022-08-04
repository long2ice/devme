from loguru import logger

from devme.enums import FrameworkType
from devme.framework.docker import Docker
from devme.settings import settings


class DockerCompose(Docker):
    type = FrameworkType.docker_compose
    image = "linuxserver/docker-compose"

    async def build(self):
        cmd = " && ".join(self.get_cmds())
        container = await self.docker.containers.run(
            config={
                "Image": self.image,
                "Cmd": ["bash", "-c", cmd],
                "HostConfig": {
                    "AutoRemove": True,
                },
                "Env": [f"DOCKER_HOST={settings.docker.host}"],
            },
            name=f"devme-{self.project_name}-builder",
        )
        async for item in container.log(stderr=True, stdout=True, follow=True):
            logger.debug(item)
        logger.success(f"run project {self.project_name} success")

    async def deploy(self):
        await self._add_reverse_proxy()

    def get_cmds(self):
        return [
            f"git clone -b {self.branch} --depth 1 {self.git_url} /src/{self.project_name}",
            f"cd /src/{self.project_name}",
            "docker-compose up -d --build",
        ]
