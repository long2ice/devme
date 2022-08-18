from enum import Enum
from typing import List, Optional

import yaml
from pydantic import AnyUrl, BaseModel, BaseSettings, HttpUrl


class Dsn(AnyUrl):
    allowed_schemes = {
        "postgres",
        "mysql",
    }
    user_required = True


class Caddy(BaseModel):
    email: str
    acme: Optional[str]
    http_port: int = 80
    https_port: int = 443
    api_port: int = 2019
    network: str = "host"
    plugins: List[str] = ["github.com/caddy-dns/alidns"]


class Network(str, Enum):
    host = "host"
    bridge = "bridge"


class Docker(BaseModel):
    host: str


class Server(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000
    url: str


class Settings(BaseSettings):
    db_url: Dsn
    debug: bool = False
    server: Server
    secret: str
    caddy: Caddy
    docker: Docker


with open("config.yaml") as f:
    settings = Settings.parse_obj(yaml.load(f, Loader=yaml.FullLoader))

TORTOISE_ORM = {
    "apps": {
        "models": {
            "models": ["devme.models", "aerich.models"],
            "default_connection": "default",
        },
    },
    "connections": {"default": settings.db_url},
}
