from fastapi import APIRouter, UploadFile, File, HTTPException
from sqlalchemy import select
from Auth.manager import current_user
from .services import upload_file, file_validator
from Pins.models import Pin
# from database import async_session

router = APIRouter()

@router.post("/createpin")
async def pin_create(title: str, desc: str, file: UploadFile = File(...)):

    if not file_validator(file):
        return HTTPException(status_code=418, detail="File not a video or image or file size > 200MB")

    await upload_file(file)

    # async with async_session() as session:
    #     session.add(Pin(title=title, desc=desc, file=file.filename))
    #     await session.commit()

    return {"file": file.filename}

@router.get("/")
async def pins_list():
    # async with async_session() as session:
    #     result = await session.execute(select(Pin))
    #     pins = result.scalars().all()
    # return pins
    pass

@router.get("/{user}")
async def pins_list_by_user(user: str):
    pass

