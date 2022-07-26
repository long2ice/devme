from enum import Enum


class FrameworkType(str, Enum):
    nodejs = "nodejs"
    html = "html"
    docker = "docker"
    docker_compose = "docker-compose"


class DeployStatus(str, Enum):
    running = "running"
    success = "success"
    failed = "failed"
    canceled = "canceled"


class GitType(str, Enum):
    github = "github"
    gitlab = "gitlab"
