import os.path
import tarfile
import tempfile
from typing import Callable, Dict, List, Optional

import aiodocker
from aiodocker import DockerError
from loguru import logger

from devme.enums import FrameworkType
from devme.framework import Framework
from devme.schema import Env
from devme.settings import settings


class Docker(Framework):
    type = FrameworkType.docker

    def __init__(
        self,
        project_name: str,
        git_url: str,
        command: str,
        domains: Optional[Dict[str, int]] = None,
        ports: Optional[Dict[int, int]] = None,
        network: str = "host",
        log_callback: Callable = None,
        image: Optional[str] = None,
        envs: Optional[List[Env]] = None,
        root: str = ".",
        ssl: bool = False,
        branch: str = "main",
    ):
        super().__init__(project_name, git_url, log_callback, image, envs, root, ssl, branch)
        self.command = command
        self.ports = ports
        self.network = network
        self.domains = domains

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
        async for item in container.log(stderr=True, stdout=True, follow=True):
            logger.debug(item)
        async with aiodocker.Docker(url=settings.docker.host) as docker:
            tar = os.path.join(tmp_dir, self.project_name, f"{self.project_name}.tar.gz")
            with tarfile.open(tar, mode="r:gz") as f:
                async for item in docker.images.build(
                    fileobj=f.fileobj,
                    encoding="gzip",
                    tag=self.project_name,
                    stream=True,
                ):
                    logger.debug(item)
        logger.success(f"build image {self.project_name} success")

    async def _add_reverse_proxy(self):
        container_name = f"devme-{self.project_name}"
        if self.domains:
            server = {}
            for domain, port in self.domains.items():
                if self.network == "host":
                    server[domain] = f"127.0.0.1:{port}"
                else:
                    server[domain] = f"{container_name}:{port}"
            return await self.caddy.add_reverse_proxy(server)

    async def deploy(self):
        host_config = {
            "RestartPolicy": {"Name": "always"},
        }
        exposed_ports: Dict[str, dict] = {}
        network_config = {}
        if self.network == "host":
            host_config["NetworkMode"] = "host"
        else:
            host_config["PortBindings"] = {}
            for host_port, container_port in self.ports.items():
                exposed_ports[f"{container_port}/tcp"] = {}
                host_config["PortBindings"][f"{container_port}/tcp"] = [
                    {"HostIP": "0.0.0.0", "HostPort": str(host_port)}
                ]
            network_config = {"EndpointsConfig": {self.network: {}}}
        container_name = f"devme-{self.project_name}"
        container = self.docker.containers.container(container_name)
        try:
            await container.stop()
            await container.delete()
        except DockerError as e:
            if e.status != 404:
                raise
        container = await self.docker.containers.run(
            config={
                "Image": self.project_name,
                "Cmd": self.command.split(" "),
                "Env": [str(env) for env in self.envs or []],
                "HostConfig": host_config,
                "NetworkingConfig": network_config,
                "ExposedPorts": exposed_ports,
            },
            name=container_name,
        )
        for item in await container.log(stderr=True, stdout=True, follow=False):
            logger.debug(item)
        await self._add_reverse_proxy()
        logger.success(f"deploy {self.project_name} success")

    def get_cmds(self):
        return [
            f"git clone -b {self.branch} --depth 1 {self.git_url} /src/{self.project_name}",
            f"cd /src/{self.project_name}",
            f"tar czf {self.project_name}.tar.gz --directory=/src/{self.source_dir} .",
        ]
