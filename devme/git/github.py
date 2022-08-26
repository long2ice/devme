from typing import List

from httpx import Headers
from loguru import logger

from devme.enums import GitType
from devme.exceptions import GetGitReposError, GetGitRepoBranchesError
from devme.git import Git
from devme.schema import Repo
from devme.settings import settings


class GitHub(Git):
    base_url = "https://api.github.com"
    type = GitType.github

    def __init__(self, token: str):
        super().__init__(token)
        self.client.headers = Headers(
            {
                "Accept": "application/vnd.github+json",
                "Authorization": f"token {token}",
            }
        )

    async def get_repos(self) -> List[Repo]:
        res = await self.client.get("/user/repos", params={"per_page": 100})
        data = res.json()
        if res.status_code != 200:
            raise GetGitReposError(data["message"])
        return [Repo.parse_obj(item) for item in data]

    async def get_branches(self, owner: str, repo: str) -> List[str]:
        res = await self.client.get(f"/repos/{owner}/{repo}/branches", params={"per_page": 100})
        data = res.json()
        if res.status_code != 200:
            raise GetGitRepoBranchesError(data["message"])
        return [item["name"] for item in data]

    async def create_webhook(self, owner: str, repo: str, callback_url: str):
        data = {
            "hub.mode": "subscribe",
            "hub.topic": f"https://github.com/{owner}/{repo}/events/push",
            "hub.callback": callback_url,
            "hub.secret": settings.secret,
        }
        res = await self.client.post("/hub", data=data)
        if res.status_code == 204:
            return
        ret = res.json()
        logger.info(ret)

    async def delete_webhook(self, owner: str, repo: str):
        data = {
            "hub.mode": "unsubscribe",
            "hub.topic": f"https://github.com/{owner}/{repo}/events/push",
        }
        res = await self.client.post("/hub", data=data)
        ret = res.json()
        logger.info(ret)
