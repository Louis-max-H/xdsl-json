from pydantic import BaseModel


class BaseBlock(BaseModel):
    type: str
