import tarfile
import tempfile
from io import BytesIO
from typing import IO, BinaryIO

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


async def build_image(email: str, https_port: int, http_port: int, api_port: int):
    caddy_file = f"""{{
    email {email}
    https_port {https_port}
    http_port {http_port}
    admin 0.0.0.0:{api_port}
}}
localhost:80 {{
    root * /usr/share/caddy
    file_server
}}
localhost:443 {{
    root * /usr/share/caddy
    file_server
}}"""
    plugins = settings.caddy.plugins
    plugins_content = " ".join(f"--with {p}" for p in plugins)
    docker_file = f"""FROM caddy:builder AS builder
RUN xcaddy build {plugins_content}

FROM caddy
COPY --from=builder /usr/bin/caddy /usr/bin/caddy
ARG CADDY_FILE
RUN echo "${{CADDY_FILE}}" > /etc/caddy/Caddyfile"""

    async with aiodocker.Docker(url=settings.docker.host) as docker:
        f = BytesIO(docker_file.encode())
        tar_obj = mktar_from_dockerfile(f)
        async for item in docker.images.build(  # type:ignore
            fileobj=tar_obj,
            encoding="gzip",
            tag=ImageName,
            stream=True,
            buildargs={"CADDY_FILE": caddy_file},
        ):
            logger.info(item)
        tar_obj.close()
