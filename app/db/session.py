from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from typing import AsyncGenerator
from app.core.config import settings

engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=True,
)

async_session_fabric = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_fabric() as session:
        yield session
