from typing import List

from devme.enums import GitType
from devme.git import Git
from devme.schema import Repo


class GitLab(Git):
    base_url = "https://gitlab.com/api/v4"
    type = GitType.gitlab

    async def create_webhook(self, owner: str, repo: str, callback_url: str):
        raise NotImplementedError

    async def delete_webhook(self, owner: str, repo: str):
        raise NotImplementedError

    async def get_repos(self) -> List[Repo]:
        raise NotImplementedError
