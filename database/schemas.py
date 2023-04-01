import uuid
from typing import List, Union, Optional
from pydantic import BaseModel


class VideoBase(BaseModel):
    """
    Schema use for Videos
    """
    sku: str
    path: Union[str, None] = None
    actress: Union[str, None] = None
    studio: Union[str, None] = None
    release_date: Union[str, None] = None
    duration: Union[int, None] = None
    cover_image: Union[str, None] = None
    images: Union[str, None] = None


class VideoCreate(VideoBase):
    pass


class Video(VideoBase):
    newly_added: bool
    view_count: int

    class Config:
        # Pydantic's orm_model allow Pydantic model
        # to read the data even if it is not a dict
        orm_mode = True


class VideoUpdate(BaseModel):
    path: Optional[str] = None
    actress: Optional[str] = None
    studio: Optional[str] = None
    release_date: Optional[str] = None
    duration: Optional[int] = None
    cover_image: Optional[str] = None
    newly_added: Optional[bool] = None
    view_count: Optional[int] = None
    images: Optional[str] = None
