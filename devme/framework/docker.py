import os.path
import tarfile
import tempfile
from typing import List, Optional, Dict

import aiodocker
from loguru import logger

from devme.framework import Framework
from devme.schema import Env
from devme.settings import settings


class Docker(Framework):
    def __init__(
        self,
        project_name: str,
        git_url: str,
        domains: List[str],
        command: str,
        ports: Optional[Dict[int, int]] = None,
        network: str = "host",
        http_port: int = 80,
        https_port: Optional[int] = 443,
        image: Optional[str] = None,
        envs: Optional[List[Env]] = None,
        root: str = ".",
    ):
        super().__init__(project_name, git_url, domains, http_port, https_port, image, envs, root)
        self.command = command
        self.ports = ports
        self.network = network

    async def build(self):
        cmd = " && ".join(self.get_cmds())
        tmp_dir = tempfile.mkdtemp()
        container = await self.docker.containers.run(
            config={
                "Image": self.image,
                "Cmd": ["bash", "-c", cmd],
                "HostConfig": {
                    "AutoRemove": True,
                    "Mounts": [{"Type": "bind", "Source": tmp_dir, "Target": "/src"}],
                },
            },
            name=f"devme-{self.project_name}-builder",
        )
        async for log in container.log(stderr=True, stdout=True, follow=True):
            logger.info(log)
        async with aiodocker.Docker(url=settings.docker.host) as docker:
            tar = os.path.join(tmp_dir, self.project_name, f"{self.project_name}.tar.gz")
            with tarfile.open(tar, mode="r:gz") as f:
                async for item in docker.images.build(
                    fileobj=f.fileobj,
                    encoding="gzip",
                    tag=self.project_name,
                    stream=True,
                ):
                    logger.info(item)

    async def deploy(self):
        host_config = {
            "RestartPolicy": {"Name": "always"},
        }
        network_config = {}
        if self.network == "host":
            host_config["NetworkMode"] = "host"
        else:
            host_config["PortBindings"] = {}
            for host_port, container_port in self.ports.items():
                host_config["PortBindings"][f"{host_port}/tcp"] = [
                    {"HostIP": "0.0.0.0", "HostPort": str(container_port)}
                ]
            network_config = {"EndpointsConfig": {self.network: {}}}
        container = await self.docker.containers.run(
            config={
                "Image": self.project_name,
                "Cmd": self.command,
                "Env": [str(env) for env in self.envs or []],
                "HostConfig": host_config,
                "NetworkingConfig": network_config,
            },
            name=f"devme-{self.project_name}",
        )
        async for log in container.log(stderr=True, stdout=True, follow=True):
            logger.info(log)

    def get_cmds(self):
        return [
            f"git clone {self.git_url} /src/{self.project_name}",
            f"cd /src/{self.project_name}",
            f"tar czf {self.project_name}.tar.gz --directory=/src/{self.source_dir} .",
        ]
