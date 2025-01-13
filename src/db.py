import sqlalchemy
import sqlalchemy.exc
from .models import Base
from typing import AsyncGenerator
from litestar import Litestar
from litestar.datastructures import State
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker,AsyncSession
from sqlalchemy import text
import os

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

@asynccontextmanager
async def init_db(app: Litestar) -> AsyncGenerator:

    engine = getattr(app, 'engine' ,None)

    if engine is None:
        engine = create_async_engine(url=DATABASE_URL, echo=True)

    async with engine.begin() as conn:
       await conn.run_sync(Base.metadata.create_all)

    app.state.engine = engine

    print("setting up")
    yield
    print("tearing down")

session_maker = async_sessionmaker(expire_on_commit=False)


async def create_session(state: State) -> AsyncGenerator[AsyncSession ,None]:
    async with session_maker(bind = state.engine) as session:
        try:
            await session.begin()
            yield session
        except sqlalchemy.exc.SQLAlchemyError as se:
            raise se