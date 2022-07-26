from copy import deepcopy
from typing import Dict, List

import httpx
from loguru import logger

from devme.exceptions import AddServerError


class Caddy:
    def __init__(self, project_name: str, host: str, port: int, ssl: bool = False):
        self.project_name = project_name
        self.client = httpx.AsyncClient(base_url=f"http://{host}:{port}/config/apps/http/servers")
        self.ssl = ssl

    async def add_route(
        self,
        route: dict,
    ):
        servers = ["srv1"]
        if self.ssl:
            servers.append("srv0")
        for server in servers:
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

    async def add_file_server(self, domains: List[str]):
        root = f"/srv/{self.project_name}"

        route = {
            "handle": [
                {"handler": "file_server", "root": root},
            ],
            "match": [{"host": domains}],
            "terminal": True,
        }

        res = await self.add_route(
            route,
        )
        if res.status_code == 500:
            raise AddServerError(res.json()["error"])
        logger.info(f"add file server, status code: {res.status_code}")

    async def add_reverse_proxy(self, servers: Dict[str, str]):
        for domain, host in servers.items():
            route = {
                "handle": [
                    {"handler": "reverse_proxy", "upstreams": [{"dial": host}]},
                ],
                "match": [{"host": [domain]}],
                "terminal": True,
            }
            res = await self.add_route(route)
            if res.status_code == 500:
                raise AddServerError(res.json()["error"])
            logger.info(f"add reverse proxy, status code: {res.status_code}")

    async def close(self):
        await self.client.aclose()
