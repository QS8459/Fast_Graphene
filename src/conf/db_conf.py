from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker
)
from src.conf.settings import settings

engine: AsyncEngine = create_async_engine(settings.db)
async_session_maker = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False
)
