import os
import uuid
import re
import time

import asyncio

from models import auth_models
from database import Session, s3_client

from pydantic import BaseModel
from typing import List, Optional

from starlette.requests import Request

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, StreamingResponse

from fastapi import APIRouter, HTTPException
from tinydb import TinyDB, Query

from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

templates = Jinja2Templates(directory="./studio/")

router = APIRouter()
db = TinyDB("users.json")
UserQuery = Query()
# app = FastAPI()

UPLOAD_DIR = "./studio/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# In-memory "database"
CLIPS_DB = []

class Clip(BaseModel):
    clip_id: str
    user_id: str
    title: str
    is_public: bool
    video_url: str
    file_path: str  # Not exposed to users in real world

# @router.get("/blocking")
async def blocking_route(start_time):
    # print("blocking world 0!")
    # await asyncio.sleep(2)
    # print("blocking world 1!")
    # await asyncio.sleep(2)
    # print("blocking world 2!")
    # await asyncio.sleep(2)
    # print("blocking world 3!")
    # await asyncio.sleep(2)
    # # time.sleep(5)
    current_timer = time.perf_counter()-start_time
    counter = 0
    while current_timer < 20:
        current_timer = time.perf_counter()-start_time
        if current_timer // 2 > counter:
            counter += 1
            print(f"counter: {counter}")
        await asyncio.sleep(0)

    return {"msg": f"Blocked yipee sequence! Time taken: {(current_timer)*1000} ms"}

@router.get("/blocking_1")
async def blocking_route_1():
    # return await blocking_route()
    return await asyncio.wait_for(blocking_route(time.perf_counter()), timeout=30)
    # return {"msg": "Blocked yipee1!"}

# @router.get("/blocking")
# def blocking_route():
#     time.sleep(5)
#     return {"msg": "Blocked yipee sync!"}

@router.get("/home")
def main(request: Request):
    if "user" not in request.session:
        return JSONResponse(status_code=403, content={"error": "Access denied"})

    url = s3_client.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': 'test-videos',
            'Key': 'demos/IMG_0743.MOV' 
        },
        ExpiresIn=3600  
    )
    # print(url)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "video_url": url
    })


@router.get("/throw_error")
def throw_error():
    raise Exception("yeeet")

@router.get("/stream/{filename}")
async def stream_video(request: Request, filename: str):
    path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")

    file_size = os.path.getsize(path)
    range_header = request.headers.get("range")
    if range_header:
        match = re.match(r"bytes=(\d+)-(\d*)", range_header)
        if match:
            start = int(match.group(1))
            end = match.group(2)
            end = int(end) if end else file_size - 1
            chunk_size = end - start + 1

            def iter_file():
                with open(path, "rb") as f:
                    f.seek(start)
                    yield f.read(chunk_size)

            return StreamingResponse(
                iter_file(),
                status_code=206,
                headers={
                    "Content-Range": f"bytes {start}-{end}/{file_size}",
                    "Accept-Ranges": "bytes",
                    "Content-Length": str(chunk_size),
                    "Content-Type": "video/mp4",
                },
            )

    # If no range header, return full file
    return FileResponse(path, media_type="video/mp4")


@router.post("/clips", response_model=Clip)
async def upload_clip(
    file: UploadFile = File(...),
    title: str = Form(...),
    is_public: bool = Form(...),
    user_id: str = Form(...),  # Simulating logged-in user
):
    clip_id = str(uuid.uuid4())
    filename = f"{clip_id}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    # Save video to disk
    with open(file_path, "wb") as f:
        f.write(await file.read())

    clip_url = f"http://localhost:8000/{file_path}"

    clip = {
        "clip_id": clip_id,
        "user_id": user_id,
        "title": title,
        "is_public": is_public,
        "video_url": clip_url,
        "file_path": file_path
    }

    CLIPS_DB.append(clip)
    return clip

@router.get("/clips", response_model=List[Clip])
def get_user_clips(user_id: str):
    return [clip for clip in CLIPS_DB if clip["user_id"] == user_id]

@router.get("/clips/{clip_id}", response_model=Clip)
def get_clip(clip_id: str):
    for clip in CLIPS_DB:
        if clip["clip_id"] == clip_id:
            return clip
    raise HTTPException(status_code=404, detail="Clip not found")

@router.delete("/clips/{clip_id}")
def delete_clip(clip_id: str):
    for i, clip in enumerate(CLIPS_DB):
        if clip["clip_id"] == clip_id:
            # Delete video file
            if os.path.exists(clip["file_path"]):
                os.remove(clip["file_path"])
            CLIPS_DB.pop(i)
            return {"detail": "Clip deleted"}
    raise HTTPException(status_code=404, detail="Clip not found")

@router.patch("/clips/{clip_id}", response_model=Clip)
def update_clip(
    clip_id: str,
    title: Optional[str] = Form(None),
    is_public: Optional[bool] = Form(None)
):
    for clip in CLIPS_DB:
        if clip["clip_id"] == clip_id:
            if title is not None:
                clip["title"] = title
            if is_public is not None:
                clip["is_public"] = is_public
            return clip
    raise HTTPException(status_code=404, detail="Clip not found")

# Optional: serve static files for local testing
@router.get("/uploads/{filename}")
def get_uploaded_file(filename: str):
    path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path)
