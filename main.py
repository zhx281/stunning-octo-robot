from typing import List, Annotated
from fastapi import FastAPI, Request, Depends, HTTPException, Form, status
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from database import crud, models, schemas
from database.database import get_db, engine

from webparser import get_info

from stream.stream import range_requests_response

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")


# Helper Function
def check_exists(sku: str, db: Session = Depends(get_db)):
    video = crud.get_video_by_sku(db, sku)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video


# Begin Routes
@app.get("/")
def home():
    return {"Hello": "world!"}


# Get All videos
@app.get("/videos", response_model=List[schemas.Video])
def read_videos(req: Request, db: Session = Depends(get_db)):
    videos = crud.get_all_videos(db)
    if not videos:
        raise HTTPException(status_code=400, detail="No video found")
    return templates.TemplateResponse("videoHome.html",
                                      {'request': req,
                                       'videos': videos})


# Display All Video with the Same Actress
@app.get("/actress/{name}", response_model=List[schemas.Video])
def read_actress(name: str, req: Request, db: Session = Depends(get_db)):
    videos = crud.get_all_videos_by_attr(db, name)
    if not videos:
        raise HTTPException(status_code=400, detail="No video found")
    return templates.TemplateResponse("videoHome.html",
                                      {'request': req,
                                       'videos': videos})


# Get single video info
@app.get("/info/{sku}", response_model=schemas.Video)
def read_video_info(sku: str, req: Request, db: Session = Depends(get_db)):
    video = crud.get_video_by_sku(db, sku)
    if not video:
        raise HTTPException(status_code=400, detail="No video found")
    return templates.TemplateResponse("updateForm.html",
                                      {'request': req,
                                       'video': video})


# Get single video
@app.get("/{sku}", response_model=schemas.Video)
def read_single_video(sku: str, db: Session = Depends(get_db)):
    video = crud.get_video_by_sku(db, sku)
    if not video:
        raise HTTPException(status_code=404,
                            detail="Video not found")
    return video


# Add all Videos
@app.get("/check/all", response_model=List[schemas.Video])
def check_folder(db: Session = Depends(get_db)):
    # Getting all videos in database
    vlist = get_info.get_videos_in_dir()
    videos = crud.get_all_videos(db)
    if videos is not None:
        skus = [video.sku for video in videos]
    else:
        skus = []
    # looping through the video in directory
    # to find new video to be created
    for v in vlist:
        _, c, n = get_info.split_sku(v)
        if f"{c}-{n}" in skus:
            continue
        # only create the sku and path
        db_video = schemas.VideoCreate(sku=f"{c}-{n}",
                                       path=get_info.get_path(v))
        crud.create_video(db, db_video)
    return RedirectResponse("/videos")


# Add one video by sku
@app.post("/add/{sku}", response_model=schemas.Video)
def add_video_by_sku(sku: str, db: Session = Depends(get_db)):
    video = crud.get_video_by_sku(db, sku)
    if video:
        raise HTTPException(status_code=400,
                            detail="Video already registered")
    video = schemas.VideoCreate(sku=sku)
    return crud.create_video(db, video)


# update video info by sku
@app.post("/update/{sku}", response_model=schemas.Video)
async def update_video_by_sku(sku: str,
                              req: Request,
                              db: Session = Depends(get_db)):
    video = crud.get_video_by_sku(db, sku)
    if not video:
        raise HTTPException(status_code=400,
                            detail="Video not found")
    form = await req.form()
    if form.get('actress') != "":
        video.actress = form.get('actress')
    if form.get('release_date') != "":
        video.release_date = form.get('release_date')
    # Assign values to video_update
    video = crud.simple_update(video, db)
    headers = {'Location': '/videos'}
    return RedirectResponse(url="/videos",
                            status_code=status.HTTP_303_SEE_OTHER,
                            headers=headers)


# Update Video
@app.get("/edit/{sku}", response_model=schemas.Video)
def update_video(sku: str, db: Session = Depends(get_db)):
    video = check_exists(sku, db)
    # Parse video info from wiki
    try:
        dic = get_info.get_video_info(sku)
    except:
        dic = {}
    is_dmm = True if get_info.split_sku(
        sku)[1] not in ['abp', 'abw'] else False
    dic['cover_image'] = get_info.get_images(sku, is_dmm=is_dmm)
    # dic['path'] = video.path
    # Assign values to video_update
    video_update = schemas.VideoInfoUpdate()
    for k, v in dic.items():
        setattr(video_update, k, v)
    # Assign update to video
    video = crud.update_video(video, db, video_update)
    return RedirectResponse(url="/videos")


# Delete Video
@app.delete("/{sku}")
def delete_video_by_sku(sku: str, db: Session = Depends(get_db)):
    video = check_exists(sku, db)
    db.delete(video)
    db.commit()
    return {"message": f"{sku} successfully deleted"}


# Stream Video
@app.get("/play/{sku}")
async def video_stream(sku: str, req: Request, db: Session = Depends(get_db)):
    # Check if the video is in the database
    video = check_exists(sku, db)
    # Get the path of the video
    path = video.path
    # Return stream data in chunks as the video play
    # with the request header informatiom as the timestamp
    return range_requests_response(req, path, "video/mp4")


# Load Cover Image
@app.get("/image/{sku}")
def display_cover_image(sku: str, db: Session = Depends(get_db)):
    video = check_exists(sku, db)
    if video.cover_image == 'string' or video.cover_image is None:
        raise HTTPException(status_code=404,
                            detail="Cover image not found")
    return FileResponse(video.cover_image, media_type='image/jpg')
