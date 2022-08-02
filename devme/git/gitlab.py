from devme.enums import GitType
from devme.git import Git


class GitLab(Git):
    base_url = "https://api.github.com"
    type = GitType.gitlab
