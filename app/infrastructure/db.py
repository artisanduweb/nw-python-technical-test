from collections.abc import AsyncGenerator

from config import get_settings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from contextlib import asynccontextmanager

Base = declarative_base()

# debug mode
debug = True
engine = create_async_engine(str(get_settings().db_url))
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    try:
        db = async_session_maker()
        yield db
    finally:
        await db.close()

