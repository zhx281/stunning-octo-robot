from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from ..webparser import get_info

from ..database import crud, schemas
from ..database.database import get_db


router = APIRouter(prefix="/reset")


@router.get("/{sku}")
def reset_video(sku: str, db: Session = Depends(get_db)):
    video = crud.get_video_by_sku(sku, db)
    if not video:
        raise HTTPException(status_code=404,
                            detail='Video not found')
    unknown = crud.get_actress_by_name('unknown', db)
    default = schemas.VideoUpdate()
    crud.update_video(video, unknown, default, db)
    for image in video.images:
        crud.delete(image, db)
    return RedirectResponse('/videos')
