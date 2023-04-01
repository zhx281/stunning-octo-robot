from sqlalchemy.orm import Session
from . import models, schemas


def get_all_videos(db: Session):
    return db.query(models.Video).all()


def get_video_by_sku(db: Session, sku: str):
    return db.query(models.Video).filter(models.Video.sku == sku).first()


def get_all_videos_by_attr(db: Session, name: str, is_search_by_studio: bool = False):
    if is_search_by_studio:
        return db.query(models.Video).filter(models.Video.studio == name).all()
    return db.query(models.Video).filter(models.Video.actress == name).all()


def create_video(db: Session, video: schemas.VideoCreate):
    db_video = models.Video(sku=video.sku,
                            path=video.path,
                            actress=video.actress,
                            studio=video.studio,
                            release_date=video.release_date,
                            duration=video.duration,
                            cover_image=video.cover_image)
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video


def update_video(model, db: Session, update_data):
    for k, v in vars(update_data).items():
        setattr(model, k, v)
    db.commit()
    db.refresh(model)
    return model
