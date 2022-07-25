from loguru import logger

from devme.caddy.volumes import VolumeSite
from devme.enums import FrameworkType
from devme.framework import Framework


class Html(Framework):
    type = FrameworkType.html

    def get_cmds(self):
        return [
            f"git clone {self.git_url} {self.project_name}",
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
        async for log in container.log(stderr=True, stdout=True, follow=True):
            logger.info(log)

    async def deploy(self):
        return await self.caddy.add_file_server()
