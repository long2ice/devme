from pydantic import BaseModel


class Env(BaseModel):
    name: str
    value: str

    def __str__(self):
        return f"{self.name}={self.value}"


class Repo(BaseModel):
    clone_url: str
    name: str
    pushed_at: str
