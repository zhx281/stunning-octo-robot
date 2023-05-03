import os
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..database import crud, models, schemas
from ..database.database import get_db

from ..stream.stream import range_requests_response

router = APIRouter(prefix="/videos")

templates = Jinja2Templates(directory="templates")


BASE_URL = os.getenv("INFO_SERVICE")


@router.get("/", response_model=list[schemas.Video])
async def display_all_videos(req: Request, db: Session = Depends(get_db)):
    # Displaying all videos in Videos directory
    videos = crud.get_all_videos(db)
    # Raise error when there is no video in database
    if not videos:
        raise HTTPException(
            status_code=404,
            detail="There is no video in database."
        )
    # Render to Jinja2 Template
    return templates.TemplateResponse("videoHome.html", {
        "request": req,
        "videos": videos,
        "base_url": BASE_URL
    })


@router.get("/{actress}", response_model=list[schemas.Video])
async def display_all_videos_by_actress(req: Request,
                                        actress: str,
                                        db: Session = Depends(get_db)):
    # Diplay videos perform by the same actress
    actress = crud.get_actress_by_name(actress, db)
    if not actress:
        raise HTTPException(status_code=404, detail="Actress not in database.")
    return templates.TemplateResponse("videoHome.html", {
        "request": req,
        "videos": actress.videos,
        "base_url": BASE_URL
    })


@router.get("/play/{sku}")
async def play_video(req: Request, sku: str, db: Session = Depends(get_db)):
    # Stream the video from server directory
    # Check if the video exist in database
    # Raise error if it is not
    video = crud.get_video_by_sku(sku, db)
    if not video:
        raise HTTPException(
            status_code=404,
            detail="Video not found."
        )
    # Partial load data to stream video
    return range_requests_response(
        req,
        f"{video.path}.mp4",
        "video/mp4")