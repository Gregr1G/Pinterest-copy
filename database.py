from fastapi import Depends
from typing import AsyncGenerator

from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]

async_engine = create_async_engine("sqlite+aiosqlite:///database.db", echo=False)

async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)

async def create_tables():
    async with async_engine.begin() as conn:
       await conn.run_sync(Base.metadata.create_all)

async def delete_tables():
   async with async_engine.begin() as conn:
       await conn.run_sync(Base.metadata.drop_all)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)