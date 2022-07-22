import aiodocker
from aiodocker import DockerError
from loguru import logger

from devme.caddy.constants import ContainerName, ImageName, Volume
from devme.caddy.volumes import Volumes
from devme.settings import settings


async def start():
    async with aiodocker.Docker(url=settings.docker.host) as docker:
        for v in Volume:
            await docker.volumes.create(
                config={
                    "Name": v,
                }
            )
        host_config = {
            "NetworkMode": "host",
            "RestartPolicy": {"Name": "always"},
            "Mounts": Volumes,
        }
        try:
            await docker.containers.run(
                config={
                    "Image": ImageName,
                    "HostConfig": host_config,
                },
                name=ContainerName,
            )
        except DockerError as e:
            if e.status == 409:
                logger.info("caddy container already exists")
                pass
            else:
                raise
        logger.success("start caddy container success")
