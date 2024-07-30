from fastapi import FastAPI
from Auth.manager import fastapi_users

from Auth.auth import auth_backend
from Auth.schemas import UserRead, UserCreate
from Pins.api import router
from contextlib import asynccontextmanager
from .models import *
from database import create_tables, delete_tables



@asynccontextmanager
async def lifespan(app: FastAPI):
   await create_tables()
   print("База готова")
   yield
   # await delete_tables()
   # print("База очищена")

app = FastAPI(lifespan=lifespan)

app.include_router(router)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
