from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

async_engine = create_async_engine("sqlite+aiosqlite:///database.db", echo=True)

async_session = async_sessionmaker(async_engine)

async def create_tables():
    async with async_engine.begin() as conn:
       await conn.run_sync(Base.metadata.create_all)

async def delete_tables():
   async with async_engine.begin() as conn:
       await conn.run_sync(Base.metadata.drop_all)