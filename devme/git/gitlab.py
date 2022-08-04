from typing import List

from devme.enums import GitType
from devme.git import Git
from devme.schema import Repo


class GitLab(Git):

    base_url = "https://api.github.com"
    type = GitType.gitlab

    async def get_repos(self) -> List[Repo]:
        pass
