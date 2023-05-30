from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

from .database import models
from .database.database import engine

from .routes import gets, updates, videos

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(gets.router)
app.include_router(updates.router)
app.include_router(videos.router)

templates = Jinja2Templates(directory="templates")


@app.get("/")
def root():
    return {"Hello": "World!"}
