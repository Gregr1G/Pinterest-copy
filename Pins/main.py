from fastapi import FastAPI
from Pins.api import router
from Pins.models import *
from contextlib import asynccontextmanager
from Pins.database import create_tables, delete_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
   await create_tables()
   print("База готова")
   yield
   await delete_tables()
   print("База очищена")

app = FastAPI(lifespan=lifespan)

app.include_router(router)