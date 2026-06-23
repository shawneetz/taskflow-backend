# Fixtures: test DB, test client, test user
import pytest
import pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.main import app
from app.db.session import get_db
from app.db.base import Base
from app.models.user import User
from app.core.security import hash_password, create_access_token
import app.models  # noqa

TEST_DB = "postgresql+asyncpg://postgres:password@localhost:5432/taskflow_test"

@pytest_asyncio.fixture(scope="session")
async def engine():
    e = create_async_engine(TEST_DB)
    async with e.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield e
    async with e.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await e.dispose()

@pytest_asyncio.fixture
async def db(engine) -> AsyncGenerator[AsyncSession, None]:
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as session:
        yield session
        await session.rollback()

@pytest_asyncio.fixture
async def client(db):
    app.dependency_overrides[get_db] = lambda: db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def test_user(db) -> User:
    user = User(email="test@example.com", hashed_password=hash_password("password123"), full_name="Test User")
    db.add(user)
    await db.commit()
    return user

@pytest_asyncio.fixture
async def auth_headers(test_user) -> dict:
    token = create_access_token(str(test_user.id))
    return {"Authorization": f"Bearer {token}"}
