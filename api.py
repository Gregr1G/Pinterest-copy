from fastapi import APIRouter, UploadFile, File, BackgroundTasks
from shutil import copyfileobj
from models import Pin
from database import async_session

router = APIRouter()

@router.post("/createpin")
async def pin_create(file: UploadFile, title: str, desc: str):
    with open(file.filename, "wb") as buffer:
        copyfileobj(file.file, buffer)

    async with async_session() as session:
        session.add(Pin(title=title, desc=desc, file=file.filename))
        await session.commit()

    return {"filename": file.filename}

@router.get("/")
def pins_list():
    return {"pins": "blabla"}