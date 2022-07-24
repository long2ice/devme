import asyncio

import pytest

from devme import caddy


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="session", autouse=True)
async def initialize():
    await caddy.start()
