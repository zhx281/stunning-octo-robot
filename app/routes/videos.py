import os
import requests
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..database import crud
from ..database.database import get_db

from ..stream.stream import range_requests_response

router = APIRouter(prefix="/videos")

templates = Jinja2Templates(directory="templates")


BASE_URL = os.getenv("INFO_SERVICE")


def get_videos(url, videos):
    skus = [_.sku for _ in videos]
    items = requests.get(url).json()
    array = []
    for item in items:
        if item['sku'] in skus:
            array.append(item)
    return array


@router.get("/")
async def display_all_actress(req: Request, db: Session = Depends(get_db)):
    videos = crud.get_all_videos(db)
    if not videos:
        return RedirectResponse('/gets/videos')
    skus = [_.sku for _ in videos]
    url = f"{BASE_URL}/all"
    items = requests.get(url).json()
    videos = []
    actress_list = []
    for item in items:
        if item['sku'] in skus:
            for actress in item['actress']:
                if actress in actress_list:
                    continue
                actress_list.append(actress)
                videos.append(item)
    return templates.TemplateResponse('videoHome.html', {
        "request": req,
        "videos": videos,
        "base_url": BASE_URL
    })


@router.get("/all")
async def display_all_videos(req: Request, db: Session = Depends(get_db)):
    videos = crud.get_all_videos(db)
    url = f"{BASE_URL}/all"
    videos = get_videos(url, videos)
    return templates.TemplateResponse('videoHome.html', {
        "request": req,
        "videos": videos,
        "base_url": BASE_URL
    })


@router.get("/{actress}")
async def all_actress_videos(req: Request, actress: str, db: Session = Depends(get_db)):
    videos = crud.get_all_videos(db)
    url = f"{BASE_URL}/actress/{actress}"
    videos = get_videos(url, videos)
    return templates.TemplateResponse('videoHome.html', {
        "request": req,
        "videos": videos,
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
        f"{video.path}",
        "video/mp4")
