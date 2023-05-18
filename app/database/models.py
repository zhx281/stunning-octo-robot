from sqlalchemy import Column, String
from .database import Base


class Video(Base):
    __tablename__ = 'videos'

    sku = Column(String, unique=True, index=True, primary_key=True)
    path = Column(String)
