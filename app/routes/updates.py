import os
import requests
from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..database import crud, schemas
from ..database.database import get_db


router = APIRouter(prefix="/update")

template = Jinja2Templates(directory="templates")

BASE_URL = os.getenv("INFO_SERVICE")


@router.get("/{sku}")
async def update_video_info(req: Request, sku: str, db: Session = Depends(get_db)):
    video = crud.get_video_by_sku(sku, db)
    if not video:
        return HTTPException(status_code=404, detail='Video not found')
    requests.post(f"{BASE_URL}/insert/{video.sku}")
    return RedirectResponse('/videos')
