import pytest

from devme import caddy


@pytest.fixture(scope="module", autouse=True)
async def start_caddy():
    await caddy.start()
