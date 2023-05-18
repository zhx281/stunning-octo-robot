from pydantic import BaseModel


class Video(BaseModel):
    sku: str
    path: str
