import os
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..database import crud, schemas
from ..database.database import get_db

router = APIRouter(prefix="/images")

templates = Jinja2Templates(directory="templates")


BASE_URL = os.getenv("INFO_SERVICE")


@router.get("/{sku}", response_model=schemas.Video)
async def display_all_videos(req: Request, sku: str, db: Session = Depends(get_db)):
    # Displaying all videos in Videos directory
    video = crud.get_video_by_sku(sku, db)
    # Raise error when there is no video in database
    if not video:
        raise HTTPException(
            status_code=404,
            detail="Video not in database."
        )
    # Render to Jinja2 Template
    return templates.TemplateResponse("images.html", {
        "request": req,
        "video": video,
        "base_url": BASE_URL
    })
