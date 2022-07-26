from enum import Enum


class FrameworkType(str, Enum):
    nodejs = "nodejs"
    html = "html"
    docker = "docker"
    docker_compose = "docker-compose"


class DeployStatus(str, Enum):
    success = "success"
    failed = "failed"
    canceled = "canceled"
