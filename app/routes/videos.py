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


def get_videos(url, videos, return_missed=False):
    """Helper function on getting all videos"""
    # List of skus in local database
    skus = {video.sku: video for video in videos}
    # Get list of videos info from host
    items = requests.get(url).json()
    # Making skus as keys for items
    sku_dic = {item['sku']: item for item in items}
    info = []
    missed = []
    # Check and return info array with either the video with or without info
    for sku in skus.keys():
        if sku in sku_dic.keys():
            info.append(sku_dic[sku])
        else:
            missed.append(skus[sku])
    if return_missed:
        return missed
    return info


@router.get("/")
async def display_all_actress(req: Request, db: Session = Depends(get_db)):
    """Video home display the most 6 recent videos"""
    videos = crud.get_all_videos(db)
    if not videos:
        return RedirectResponse('/get/videos')
    # Getting all sku from local database
    skus = [_.sku for _ in videos]
    # Getting all info from host database with request
    url = f"{BASE_URL}/all"
    items = requests.get(url).json()
    # Assign matching sku to videos
    videos = [item for item in items if item['sku'] in skus]
    return templates.TemplateResponse('videoHome.html', {
        "request": req,
        "videos": videos[:6],
        "base_url": BASE_URL
    })


@router.get("/all")
async def display_all_videos(req: Request, db: Session = Depends(get_db)):
    """Display all videos in that can be viewed"""
    videos = crud.get_all_videos(db)
    url = f"{BASE_URL}/all"
    videos = get_videos(url, videos)
    return templates.TemplateResponse('videoHome.html', {
        "request": req,
        "videos": videos,
        "base_url": BASE_URL
    })


@router.get("/missing-info")
async def display_missing_info(req: Request, db: Session = Depends(get_db)):
    """Display all videos that needs info"""
    videos = crud.get_all_videos(db)
    url = f"{BASE_URL}/all"
    videos = get_videos(url, videos, return_missed=True)
    return templates.TemplateResponse('videoHome.html', {
        "request": req,
        "videos": videos,
        "base_url": BASE_URL
    })


@router.get("/{actress}")
async def all_actress_videos(req: Request, actress: str, db: Session = Depends(get_db)):
    """Display all video that the actress perfomed in"""
    videos = crud.get_all_videos(db)
    url = f"{BASE_URL}/actress/{actress}"
    videos = get_videos(url, videos)
    return templates.TemplateResponse('videoHome.html', {
        "request": req,
        "videos": videos,
        "base_url": BASE_URL
    })


@router.get("/play/{sku}")
async def play_video(req: Request, sku: str):
    """Render page with video player"""
    return templates.TemplateResponse('videoPlay.html', {
        "request": req,
        "sku": sku
    })


@router.get("/stream/{sku}")
async def stream_video(req: Request, sku: str, db: Session = Depends(get_db)):
    """Streaming the video"""
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
