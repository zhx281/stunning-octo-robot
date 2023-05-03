from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from ..webparser import get_info

from ..database import crud, schemas
from ..database.database import get_db


router = APIRouter(prefix="/get")


@router.get("/videos")
async def get_all_videos(db: Session = Depends(get_db)):
    # Look up videos in Videos' directory
    video_list = get_info.get_videos_in_dir()
    # Check for default unknow actress
    # if not create default actress
    actress = crud.get_actress_by_name('unknown', db)
    if not actress:
        actress = crud.create_default_actress(db)
    # Loop through videos and create each video
    # If the video already exist in database
    # skip it
    for name in video_list:
        _, a, c = get_info.split_sku(name)
        sku = f"{a}-{c}"
        path = get_info.get_path(sku)
        video = crud.get_video_by_sku(sku, db)
        if video:
            continue
        crud.create_video(sku, path, actress.id, actress.name, db)
    # Redirect to /videos path
    return RedirectResponse(url="/videos")


@router.get("/info/{sku}")
async def get_video_info(sku: str, db: Session = Depends(get_db)):
    # Get video info from informer
    info = get_info.look_at_informer(sku)
    # Split the sample image into it's own dictionary
    images = info.pop('sample_images')
    # Check if there is actress info from wiki
    # if not keep assign to unknown
    if 'actress' in info.keys():
        # Search for actress in actor table
        # if not in actor table create new actress
        actress = crud.get_actress_by_name(info['actress'], db)
        if not actress:
            splited_name = info['actress'].split(' ')
            if len(splited_name) == 2:
                last_name, first_name = info['actress'].split(' ')
            else:
                last_name = ''
                first_name = ''
            actress_create = schemas.ActorCreate(
                name=info['actress'],
                first_name=first_name,
                last_name=last_name
            )
            actress = crud.create_actress(actress_create, db)
        # Add info to video update
        video_update = schemas.VideoUpdate(
            studio=info['studio'],
            duration=info['duration'],
            release_date=info['release_date'],
            cover_image=info['cover_image']
        )
    else:
        actress = crud.get_actress_by_name('unknown', db)
        # Only adding cover_image because it's from a different database
        video_update = schemas.VideoUpdate(cover_image=info['cover_image'])
    # Check if the video is in database
    # Raise error if not
    video = crud.get_video_by_sku(sku, db)
    if not video:
        raise HTTPException(status_code=404, detail="Video not find.")
    # Update the video in database
    video = crud.update_video(video, actress, video_update, db)
    # Looping through images and add to database
    for k, v in images.items():
        # Check if the image already exist in database
        # if it is continue to the next one
        image = crud.get_image_by_name(k, db)
        if image:
            continue
        # Add image to database
        image = crud.create_image(f"{sku}-{k}", v, video, db)
    # Redirect to /videos path
    return RedirectResponse(url="/videos")
