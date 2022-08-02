from typing import List

from devme.enums import GitType
from devme.git import Git
from devme.schema import Repo


class GitHub(Git):
    base_url = "https://api.github.com"
    type = GitType.github

    def __init__(self, token: str):
        super().__init__(token)
        self.client.headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"token {token}",
        }

    async def get_repos(self) -> List[Repo]:
        res = await self.client.get("/user/repos")
        data = res.json()
        return [Repo.parse_obj(item) for item in data]
