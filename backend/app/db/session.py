from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (
	AsyncSession,
	async_sessionmaker,
	create_async_engine,
)

from app.core.config import settings

engine = create_async_engine(
	settings.database_url,
	echo=settings.debug,
	pool_pre_ping=True,
	pool_size=settings.db_pool_size,
	max_overflow=settings.db_max_overflow,
	pool_recycle=settings.db_pool_recycle_seconds,
)

AsyncSessionLocal = async_sessionmaker(
	bind=engine,
	class_=AsyncSession,
	expire_on_commit=False,
	autoflush=False,
)


async def get_db() -> AsyncIterator[AsyncSession]:
	async with AsyncSessionLocal() as session:
		try:
			yield session
		finally:
			await session.close()
