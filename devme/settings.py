from enum import Enum

import yaml
from pydantic import AnyUrl, BaseModel, BaseSettings


class Dsn(AnyUrl):
    allowed_schemes = {
        "postgres",
        "mysql",
    }
    user_required = True


class Caddy(BaseModel):
    http_port: str
    https_port: str
    api_port: str


class Network(str, Enum):
    host = "host"
    bridge = "bridge"


class Docker(BaseModel):
    host: str
    network: Network


class Settings(BaseSettings):
    db_url: Dsn
    caddy: Caddy
    docker: Docker

    @property
    def is_host_mode(self):
        return self.docker.network == Network.host


with open("config.yaml") as f:
    settings = Settings.parse_obj(yaml.load(f, Loader=yaml.FullLoader))
