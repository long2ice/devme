import pytest

from devme.caddy.image import build_image


@pytest.mark.asyncio
async def test_build_image():
    await build_image("long2ice@gmail.com", 443, 80, 2019)
