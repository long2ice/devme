from pydantic import BaseModel

from devme.enums import FrameworkType


class FrameworkInfo(BaseModel):
    type: FrameworkType
    image: str
