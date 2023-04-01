from sqlalchemy import Column, Boolean, String, Integer
from sqlalchemy.sql import func

from .database import Base


class Video(Base):
    __tablename__ = 'videos'

    id = Column(Integer,
                primary_key=True,
                index=True,
                server_default=func.nextval('tags_id_seq'))
    sku = Column(String, unique=True, index=True)
    path = Column(String)
    actress = Column(String)
    studio = Column(String)
    release_date = Column(String)
    duration = Column(String)
    cover_image = Column(String)
    newly_added = Column(Boolean, default=True)
    view_count = Column(Integer, default=0)
    images = Column(String)
