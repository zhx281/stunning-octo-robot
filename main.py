from typing import List
from fastapi import FastAPI, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from database import crud, models, schemas
from database.database import get_db, engine

from webparser import get_info

from stream.stream import range_requests_response

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home():
    return {"Hello": "world!"}


# Get All videos
@app.get("/videos", response_model=List[schemas.Video])
def read_videos(db: Session = Depends(get_db)):
    videos = crud.get_all_videos(db)
    return videos


# Get single video
@app.get("/{sku}", response_model=schemas.Video)
def read_single_video(sku: str, db: Session = Depends(get_db)):
    video = crud.get_video_by_sku(db, sku)
    if not video:
        raise HTTPException(status_code=404,
                            detail="Video not found")
    return video


# Add Videos
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
    return crud.get_all_videos(db)


# Update Video
@app.put("/edit/{sku}", response_model=schemas.Video)
def update_video(sku: str, video_update: schemas.VideoUpdate, db: Session = Depends(get_db)):
    video = crud.get_video_by_sku(db, sku)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    # Parse video info from wiki
    dic = get_info.get_video_info(sku)
    is_dmm = True if get_info.split_sku(
        sku)[1] not in ['abp', 'abw'] else False
    dic['cover_image'] = get_info.get_images(sku, is_dmm=is_dmm)
    # Assign values to video_update
    for k, v in dic.items():
        setattr(video_update, k, v)
    # Assign update to video
    video = crud.update_video(video, db, video_update)
    return video


# Delete Video
@app.delete("/{sku}")
def delete_video_by_sku(sku: str, db: Session = Depends(get_db)):
    video = crud.get_video_by_sku(db, sku)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    db.delete(video)
    db.commit()
    return {"message": f"{sku} successfully deleted"}


# Stream Video
@app.get("/play/{sku}")
async def video_stream(sku: str, req: Request, db: Session = Depends(get_db)):
    # Check if the video is in the database
    video = crud.get_video_by_sku(db, sku)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    # Get the path of the video
    path = video.path
    # Return stream data in chunks as the video play
    # with the request header informatiom as the timestamp
    return range_requests_response(req, path, "video/mp4")
