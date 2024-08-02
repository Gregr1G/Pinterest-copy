from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy import select
from Auth.manager import current_user
from Pins.services import upload_file, file_validator
from Pins.models import Pin
from database import async_session_maker as async_session, User
from Pins.redis_client import redis_client

router = APIRouter()

@router.post("/createpin")
async def pin_create(title: str, desc: str, file: UploadFile = File(...), user: User = Depends(current_user)):

    if not file_validator(file):
        return HTTPException(status_code=418, detail="File not a video or image or file size > 200MB")

    await upload_file(file)

    async with async_session() as session:
        new_pin = Pin(title=title, desc=desc, file=file.filename, creator=user.id)
        session.add(new_pin)
        await session.flush()

        await redis_client.set(f"{new_pin.id}", 1)
        await session.commit()
    return {"file": file.filename, "creator": user}

@router.get("/")
async def pins_list():
    async with async_session() as session:
        result = await session.execute(select(Pin))
        pins = result.scalars().all()
    return pins

@router.get("/{user}")
async def pins_list_by_user(user: int):
    async with async_session() as session:
        result = select(Pin).where(Pin.creator == user)
        users_pins = await session.execute(result)
    return users_pins.scalars().all()

@router.post("/{pin}")
async def retrieve_pin(pin: int):
    views = await redis_client.incr(f"{pin}")

    async with async_session() as session:
        result = select(Pin).where(Pin.id == pin)
        pinn = await session.execute(result)

    return {"views": views, "pin": pinn.scalars().one()}


