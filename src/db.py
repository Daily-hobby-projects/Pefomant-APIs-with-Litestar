from .models import Base
from typing import AsyncGenerator
from litestar import Litestar
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
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

    print("setting up")
    yield
    print("tearing down")