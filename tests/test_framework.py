import pytest

from devme.framework.html import Html
from devme.framework.nodejs import NodeJS


@pytest.mark.asyncio
async def test_nodejs():
    n = NodeJS(
        "telsearch",
        "https://github.com/telsearch/telsearch-web.git",
        domains=["telsearch.long2ice.io"],
        https_port=None,
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
        https_port=None,
    )
    # await n.build()
    await n.deploy()
    await n.clear()
