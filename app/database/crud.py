from sqlalchemy.orm import Session
from . import models, schemas


def get_all_videos(db):
    return db.query(models.Video).order_by(models.Video.sku).all()


def get_video_by_sku(sku: str, db: Session):
    return db.query(models.Video).filter(models.Video.sku == sku).first()


def create_video(sku: str, path: str, db: Session):
    db_video = models.Video(sku=sku,
                            path=path)
    return add_to_database(db_video, db)


def add_to_database(model, db: Session):
    db.add(model)
    db.commit()
    return reload(model, db)


def reload(model, db: Session):
    db.refresh(model)
    return model


def delete(model, db: Session):
    db.delete(model)
    db.commit()
