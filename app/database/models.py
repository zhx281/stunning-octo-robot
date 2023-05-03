from sqlalchemy import Column, Boolean, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Actor(Base):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    first_name = Column(String)
    last_name = Column(String)

    videos = relationship('Video', back_populates='owner')


class Video(Base):
    __tablename__ = 'videos'

    sku = Column(String, unique=True, index=True, primary_key=True)
    path = Column(String)
    actress = Column(String)
    studio = Column(String)
    release_date = Column(String)
    duration = Column(String)
    cover_image = Column(String)

    owner_id = Column(Integer, ForeignKey("actors.id"))
    owner = relationship("Actor", back_populates="videos")

    images = relationship('Image', back_populates="owner")


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    image = Column(String)

    owner_id = Column(String, ForeignKey("videos.sku"))
    owner = relationship("Video", back_populates="images")
