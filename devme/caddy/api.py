from typing import List

import httpx


class Caddy:
    def __init__(self, port: int):
        self.client = httpx.AsyncClient(base_url=f"http://localhost:{port}")

    async def add_file_server(self, domains: List[str], root: str):
        res = await self.client.patch(
            "/config/apps/http/servers/srv0/routes",
            json={
                "handle": [
                    {
                        "handler": "subroute",
                        "routes": [
                            {
                                "handle": [
                                    {
                                        "handler": "subroute",
                                        "routes": [
                                            {
                                                "handle": [
                                                    {
                                                        "handler": "vars",
                                                        "root": root,
                                                    }
                                                ]
                                            },
                                            {
                                                "handle": [
                                                    {
                                                        "handler": "file_server",
                                                        "hide": ["/etc/caddy/Caddyfile"],
                                                    }
                                                ]
                                            },
                                        ],
                                    }
                                ]
                            }
                        ],
                    }
                ],
                "match": [{"host": [domains]}],
                "terminal": True,
            },
        )
        return res.json()

    async def close(self):
        await self.close()
