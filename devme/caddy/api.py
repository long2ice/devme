from copy import deepcopy
from typing import List, Optional

import httpx
from loguru import logger

from devme.caddy.exceptions import AddServerError


class Caddy:
    def __init__(
        self,
        domains: List[str],
        project_name: str,
        host: str,
        port: int,
        http_port: int = 80,
        https_port: Optional[int] = 443,
    ):
        self.project_name = project_name
        self.https_port = https_port
        self.http_port = http_port
        self.client = httpx.AsyncClient(base_url=f"http://{host}:{port}/config/apps/http/servers")
        self.domains = domains

    async def add_route(
        self,
        route: dict,
    ):
        if self.https_port:
            server = "srv0"
        else:
            server = "srv1"
        res = await self.client.get(f"/{server}/routes")
        routes = res.json()
        copy_routes = deepcopy(routes)
        for i, r in enumerate(routes):
            if r["handle"] == route["handle"]:
                copy_routes[i] = route
                break
        else:
            copy_routes.append(route)
        return await self.client.patch(f"/{server}/routes", json=copy_routes)

    async def add_file_server(
        self,
    ):
        root = f"/srv/{self.project_name}"

        route = {
            "handle": [
                {"handler": "file_server", "root": root},
            ],
            "match": [{"host": self.domains}],
            "terminal": True,
        }

        res = await self.add_route(
            route,
        )
        if res.status_code == 500:
            raise AddServerError(res.json()["error"])
        logger.info(f"add file server, status code: {res.status_code}")

    async def add_reverse_proxy(self, server: str):
        route = {
            "handle": [
                {"handler": "reverse_proxy", "upstreams": [{"dial": server}]},
            ],
            "match": [{"host": self.domains}],
            "terminal": True,
        }
        res = await self.add_route(route)
        if res.status_code == 500:
            raise AddServerError(res.json()["error"])
        logger.info(f"add reverse proxy, status code: {res.status_code}")

    async def close(self):
        await self.client.aclose()
