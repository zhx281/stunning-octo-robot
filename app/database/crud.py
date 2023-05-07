from sqlalchemy.orm import Session
from . import models, schemas


def get_image_by_owner(owner_id: str, db: Session):
    return db.query(models.Image).filter(
        models.Image.owner_id == owner_id).order_by(models.Image.name).all()


def get_image_by_name(name: str, db: Session):
    return db.query(models.Image).filter(models.Image.name == name).first()


def create_image(name: str, path: str, video: models.Video, db: Session):
    db_image = models.Image(name=name, image=path, owner_id=video.sku)
    return add_to_database(db_image, db)


def get_all_videos(db):
    return db.query(models.Video).order_by(models.Video.sku).all()


def get_video_by_sku(sku: str, db: Session):
    return db.query(models.Video).filter(models.Video.sku == sku).first()


def get_video_by_actress(aid: int, db: Session):
    return db.query(models.Video).filter(models.Video.owner_id == aid).order_by(models.Video.sku).all()


def create_video(sku: str, path: str, actor_id: int, actor_name: str, db: Session):
    db_video = models.Video(sku=sku,
                            path=path,
                            actress=actor_name,
                            owner_id=actor_id)
    return add_to_database(db_video, db)


def update_video(video: models.Video,
                 actress: models.Actor,
                 video_update: schemas.VideoUpdate,
                 db: Session):
    for k, v in video_update.dict().items():
        setattr(video, k, v)
    video.owner_id = actress.id
    video.actress = actress.name
    return add_to_database(video, db)


def update_partial_video(video: models.Video,
                         video_update: schemas.VideoUpdate,
                         db: Session):
    for k, v in video_update.dict().items():
        setattr(video, k, v)
    return add_to_database(video, db)


def get_all_actress(db: Session):
    return db.query(models.Actor).order_by(models.Actor.last_name).all()


def get_actress_by_name(name: str, db: Session):
    return db.query(models.Actor).filter(models.Actor.name == name).first()


def create_default_actress(db: Session):
    db_actress = models.Actor(name="unknown",
                              first_name="unknown",
                              last_name="unknown")
    return add_to_database(db_actress, db)


def create_actress(actor: schemas.ActorCreate, db: Session):
    db_actress = models.Actor(**actor.dict())
    return add_to_database(db_actress, db)


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
