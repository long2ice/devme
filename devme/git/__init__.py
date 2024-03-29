import abc
from typing import List

import httpx

from devme.enums import GitType
from devme.schema import Repo


class Git:
    type: GitType
    base_url: str

    def __init__(self, token: str):
        self.client = httpx.AsyncClient(base_url=self.base_url)
        self.token = token

    @abc.abstractmethod
    async def get_repos(self) -> List[Repo]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_branches(self, owner: str, repo: str) -> List[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def create_webhook(self, owner: str, repo: str, callback_url: str):
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_webhook(
        self,
        owner: str,
        repo: str,
    ):
        raise NotImplementedError
