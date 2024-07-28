from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from sqlalchemy import select

from services import upload_file, file_validator
from models import Pin
from database import async_session

router = APIRouter()

@router.post("/createpin")
async def pin_create(title: str, desc: str, file: UploadFile = File(...)):

    if not file_validator(file):
        return HTTPException(status_code=418, detail="File not a video or image or file size > 200MB")

    await upload_file(file)

    async with async_session() as session:
        session.add(Pin(title=title, desc=desc, file=file.filename))
        await session.commit()

    return {"file": file}

@router.get("/")
async def pins_list():
    async with async_session() as session:
        result = await session.execute(select(Pin))
        pins = result.scalars().all()
    return pins

@router.get("/user")
async def pins_list_by_user():
    pass

