from pydantic import BaseModel


class Env(BaseModel):
    name: str
    value: str

    def __str__(self):
        return f"{self.name}={self.value}"
