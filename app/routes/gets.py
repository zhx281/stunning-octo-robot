import os
import requests
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from ..database import crud
from ..database.database import get_db


router = APIRouter(prefix="/get")


@router.get("/videos")
async def get_all_videos(db: Session = Depends(get_db), force: bool = False):
    """Get all videos in folders"""
    video_path = os.getenv("VIDEO_PATH")
    files = os.listdir(video_path)
    for file in files:
        if ".mp4" in file:
            sku = file.split('.mp4')[0].lower()
            if '-c' in sku:
                sku = sku.replace('-c', '')
            # Check if sku in database
            item = crud.get_video_by_sku(sku, db)
            if item and not force:
                continue
            # Setup new item
            elif item is not None:
                path = os.path.join(video_path, file)
                crud.create_video(sku=sku, path=path, db=db)
            elif force:
                requests.post(f'{os.getenv("BASE_URL")}/insert/{sku}')
    return RedirectResponse('/videos')
