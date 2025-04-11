from sqlalchemy.ext.asyncio import AsyncSession
from src.conf.db_conf import async_session_maker
from src.conf.di import di


async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session

di.register_async(AsyncSession, get_session)
