# Создание сессии
# SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
# engine = create_engine(SQLALCHEMY_DATABASE_URI)
# Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from python_test.settings import settings

# Подключение базы (с автоматической генерацией моделей)


sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True,
    pool_size=5,
    max_overflow=10
)
async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
    # pool_size=5,
    # max_overflow=10
)

SyncSession = sessionmaker(bind=sync_engine, autocommit=False)

MyAsyncSession = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)


def get_db() -> Generator:
    try:
        session: SyncSession = SyncSession()
        yield session
    finally:
        session.close()


async def get_async_db() -> Generator:
    try:
        session: AsyncSession = MyAsyncSession()
        yield session
    finally:
        await session.close()
