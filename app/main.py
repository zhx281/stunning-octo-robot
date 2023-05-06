from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

from .database import models
from .database.database import engine

from .routes import gets, updates, resets, videos, images

from .webparser import get_info

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(gets.router)
app.include_router(updates.router)
app.include_router(resets.router)
app.include_router(videos.router)
app.include_router(images.router)

templates = Jinja2Templates(directory="templates")


@app.get("/")
def root():
    return RedirectResponse("/videos")


@app.get("/test")
def test():
    path = '/home/dx/Videos/ipzz-021.mp4'
    return get_info.get_video_duration(path)
