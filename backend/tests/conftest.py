# ruff: noqa: E402
import os

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

os.environ["DATABASE_URL"] = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/testdb",
)

import app.db.models  # noqa: F401  # регистрация моделей
from app.core.database import get_db_session
from app.db.base import Base

TEST_DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def override_get_db():
    async with TestSessionLocal() as session:
        yield session


@pytest_asyncio.fixture(scope="session")
async def test_app():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    from app.main import app

    app.dependency_overrides[get_db_session] = override_get_db
    return app


@pytest_asyncio.fixture(scope="function")
async def db_session(test_app):
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(scope="function")
async def client(test_app, db_session):
    async with AsyncClient(
        transport=ASGITransport(app=test_app), base_url="http://test"
    ) as ac:
        yield ac
