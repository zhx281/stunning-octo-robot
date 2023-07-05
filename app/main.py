from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

from .database import models
from .database.database import engine

from .routes import gets, updates, videos, admins

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(gets.router)
app.include_router(updates.router)
app.include_router(videos.router)
app.include_router(admins.router)

templates = Jinja2Templates(directory="templates")


@app.get("/")
def root():
    return {"Hello": "World!"}
