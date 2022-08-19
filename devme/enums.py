from enum import Enum


class FrameworkType(str, Enum):
    nodejs = "NodeJS"
    html = "html"
    docker = "Docker"
    docker_compose = "docker-compose"


class DeployStatus(str, Enum):
    running = "running"
    success = "success"
    failed = "failed"
    canceled = "canceled"


class GitType(str, Enum):
    github = "github"
    gitlab = "gitlab"
