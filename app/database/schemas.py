from typing import Union
from pydantic import BaseModel


class ImageBase(BaseModel):
    name: str
    image: str


class ImageCreate(ImageBase):
    pass


class ImageUpdate(ImageBase):
    pass


class Image(ImageBase):
    id: int
    owner_id: str

    class Config:
        orm_mode = True


class VideoBase(BaseModel):
    studio: Union[str, None] = None
    release_date: Union[str, None] = None
    duration: Union[int, None] = None
    cover_image: Union[str, None] = None


class VideoCreate(VideoBase):
    pass


class VideoUpdate(VideoBase):
    pass


class Video(VideoBase):
    sku: str
    actress: str
    path: Union[str, None] = None
    images: list[Image] = []
    owner_id = int

    class Config:
        orm_mode = True


class ActorBase(BaseModel):
    name: Union[str, None] = None
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None


class ActorCreate(ActorBase):
    pass


class ActorUpdate(ActorBase):
    pass


class Actor(ActorBase):
    id: int
    videos: list[Video] = []

    class Config:
        orm_mode = True
