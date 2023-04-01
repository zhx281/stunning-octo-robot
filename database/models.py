from sqlalchemy import Column, Boolean, String, Integer
from .database import Base


class Video(Base):
    __tablename__ = 'videos'

    sku = Column(String, unique=True, index=True, primary_key=True)
    path = Column(String)
    actress = Column(String)
    studio = Column(String)
    release_date = Column(String)
    duration = Column(String)
    cover_image = Column(String)
    newly_added = Column(Boolean, default=True)
    view_count = Column(Integer, default=0)
    images = Column(String)
