import pytest

from devme.framework.docker import Docker
from devme.framework.docker_compose import DockerCompose
from devme.framework.html import Html
from devme.framework.nodejs import NodeJS


@pytest.mark.asyncio
async def test_nodejs():
    n = NodeJS(
        "telsearch",
        "https://github.com/telsearch/telsearch-web.git",
        domains=["telsearch.long2ice.io"],
    )
    # await n.build()
    await n.deploy()
    await n.clear()


@pytest.mark.asyncio
async def test_html():
    n = Html(
        "sponsor",
        "https://github.com/long2ice/sponsor.git",
        domains=["sponsor.long2ice.io"],
    )
    # await n.build()
    await n.deploy()
    await n.clear()


@pytest.mark.asyncio
async def test_docker():
    n = Docker(
        "gema",
        "https://github.com/long2ice/gema.git",
        domains={"gema.long2ice.io": 8000},
        root=".",
        command="uvicorn gema.app:app --host 0.0.0.0",
        network="devme",
        ports={8000: 8000},
    )
    await n.build()
    await n.deploy()
    await n.clear()


@pytest.mark.asyncio
async def test_docker_compose():
    n = DockerCompose(
        "gema",
        "https://github.com/long2ice/gema.git",
        domains={"gema.long2ice.io": 8000},
        root=".",
        command="uvicorn gema.app:app --host 0.0.0.0",
        network="devme",
        ports={8000: 8000},
    )
    await n.build()
    await n.deploy()
    await n.clear()
