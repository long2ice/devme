import tarfile
import tempfile
from io import BytesIO
from typing import IO, BinaryIO, Optional

import aiodocker
from loguru import logger

from devme.caddy.constants import ImageName
from devme.settings import settings


def mktar_from_dockerfile(fileobject: BinaryIO) -> IO:
    f = tempfile.NamedTemporaryFile()
    t = tarfile.open(mode="w:gz", fileobj=f)

    if isinstance(fileobject, BytesIO):
        dfinfo = tarfile.TarInfo("Dockerfile")
        dfinfo.size = len(fileobject.getvalue())
        fileobject.seek(0)
    else:
        dfinfo = t.gettarinfo(fileobj=fileobject, arcname="Dockerfile")

    t.addfile(dfinfo, fileobject)
    t.close()
    f.seek(0)
    return f


async def build_image(
    email: str, https_port: int, http_port: int, api_port: int, acme: Optional[str] = None
):
    caddy_file = f"""{{
    email {email}
    https_port {https_port}
    http_port {http_port}
    admin 0.0.0.0:{api_port}
    {acme or ""}
}}
localhost:{http_port} {{
    root * /usr/share/caddy
    file_server
}}
localhost:{https_port} {{
    root * /usr/share/caddy
    file_server
}}"""
    plugins = settings.caddy.plugins
    plugins_content = " ".join(f"--with {p}" for p in plugins)
    caddy_builder = "caddy:builder"
    docker_file = f"""FROM {caddy_builder} AS builder
RUN xcaddy build {plugins_content}

FROM caddy
COPY --from=builder /usr/bin/caddy /usr/bin/caddy
ARG CADDY_FILE
RUN echo "${{CADDY_FILE}}" > /etc/caddy/Caddyfile"""

    async with aiodocker.Docker(url=settings.docker.host) as docker:
        async for item in docker.pull(caddy_builder, stream=True):
            logger.debug(item)
        logger.success(f"pull image {caddy_builder} success")
        f = BytesIO(docker_file.encode())
        tar_obj = mktar_from_dockerfile(f)
        async for item in docker.images.build(  # type:ignore
            fileobj=tar_obj,
            encoding="gzip",
            tag=ImageName,
            stream=True,
            buildargs={"CADDY_FILE": caddy_file},
        ):
            logger.debug(item)
        tar_obj.close()
        logger.success(f'build caddy image with plugins: {", ".join(plugins)} success')
