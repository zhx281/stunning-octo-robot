from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

from .database import models
from .database.database import engine

from .routes import gets, updates, resets, videos, images


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
    return {"message": "Welcome"}
