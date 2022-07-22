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
            "NetworkMode": settings.docker.network,
            "RestartPolicy": {"Name": "always"},
            "Mounts": Volumes,
        }
        if not settings.is_host_mode:
            host_config["PortBindings"] = {
                "80/tcp": [{"HostIP": "0.0.0.0", "HostPort": settings.caddy.http_port}],
                "443/tcp": [{"HostIP": "0.0.0.0", "HostPort": settings.caddy.https_port}],
                "2019/tcp": [{"HostIP": "0.0.0.0", "HostPort": settings.caddy.api_port}],
            }
        try:
            container = await docker.containers.run(
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
