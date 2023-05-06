import os
from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..webparser import get_info

from ..database import crud, schemas
from ..database.database import get_db


router = APIRouter(prefix="/update")

template = Jinja2Templates(directory="templates")


@router.get("/{sku}", response_model=schemas.Video)
async def show_video_info(req: Request, sku: str, db: Session = Depends(get_db)):
    video = crud.get_video_by_sku(sku, db)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found.")

    video_update = schemas.VideoUpdate(**video.__dict__)

    return template.TemplateResponse("updateForm.html", {
        "request": req,
        "video": video,
        "video_dict": video_update.dict(),
        "base_url": os.getenv("INFO_SERVICE")
    })


@router.post("/{sku}")
async def update_video_info(req: Request, sku: str, db: Session = Depends(get_db)):
    video = crud.get_video_by_sku(sku, db)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found.")
    form = await req.form()
    form = form.__dict__['_dict']
    form['duration'] = get_info.convert_duration(form['duration'])
    form['release_date'] = get_info.convert_release_date(form['release_date'])
    actress_name = form.pop('actress')
    # Check if actress change
    if actress_name != video.actress:
        actress = crud.get_actress_by_name(actress_name, db)
        if not actress:
            splited_name = actress_name.split(' ')
            if len(splited_name) == 2:
                last_name, first_name = actress_name.split(' ')
            else:
                last_name = ''
                first_name = ''
            actress_model = schemas.ActorCreate(
                name=actress_name,
                first_name=first_name,
                last_name=last_name
            )
            actress = crud.create_actress(actress_model, db)
        video.owner_id = actress.id
        video.actress = actress.name
    # Update video info
    for k, v in form.items():
        setattr(video, k, v)
    video = crud.add_to_database(video, db)
    headers = {'Location': '/videos'}
    return RedirectResponse(url="/videos",
                            status_code=status.HTTP_303_SEE_OTHER,
                            headers=headers)
