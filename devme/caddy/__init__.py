import aiodocker
from aiodocker import DockerError
from loguru import logger

from devme.caddy.constants import ContainerName, ImageName, Volume
from devme.caddy.image import build_image
from devme.caddy.volumes import Volumes
from devme.settings import settings


async def start():
    http_port = settings.caddy.http_port
    https_port = settings.caddy.https_port
    api_port = settings.caddy.api_port
    await build_image(settings.caddy.email, https_port, http_port, api_port)
    async with aiodocker.Docker(url=settings.docker.host) as docker:
        for v in Volume:
            await docker.volumes.create(
                config={
                    "Name": v,
                }
            )
        host_config = {
            "RestartPolicy": {"Name": "always"},
            "Mounts": Volumes,
        }
        network_config = {}
        network = settings.caddy.network

        if network == "host":
            host_config["NetworkMode"] = "host"
        else:
            host_config["PortBindings"] = {
                f"{http_port}/tcp": [{"HostIP": "0.0.0.0", "HostPort": str(http_port)}],
                f"{https_port}/tcp": [{"HostIP": "0.0.0.0", "HostPort": str(https_port)}],
                f"{api_port}/tcp": [{"HostIP": "0.0.0.0", "HostPort": str(api_port)}],
            }
            network_config = {"EndpointsConfig": {network: {}}}
        try:
            await docker.containers.run(
                config={
                    "Image": ImageName,
                    "HostConfig": host_config,
                    "NetworkingConfig": network_config,
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
