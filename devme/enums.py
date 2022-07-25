from enum import Enum


class FrameworkType(str, Enum):
    nodejs = "nodejs"
    html = "html"


class DeployStatus(str, Enum):
    success = "success"
    failed = "failed"
    canceled = "canceled"
