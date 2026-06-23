# Fixtures: test DB, test client, test user

import pytest
import pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.main import app as fastapi_app   # ← alias to avoid name collision
from app.db.session import get_db
from app.db.base import Base
from app.models.user import User
from app.core.security import hash_password, create_access_token
import app.models  # noqa — registers all models with Base.metadata

TEST_DB = "postgresql+asyncpg://postgres:Ichika01@localhost:5433/taskflow_test"

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
    async with engine.connect() as connection:
        transaction = await connection.begin()
        session = AsyncSession(
            bind=connection,
            expire_on_commit=False,
            join_transaction_mode="create_savepoint",
        )
        yield session
        await session.close()
        await transaction.rollback()

@pytest_asyncio.fixture
async def client(db):
    async def override_get_db():
        yield db

    fastapi_app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as c:
        yield c
    fastapi_app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def test_user(db) -> User:
    user = User(
        email="test@example.com",
        hashed_password=hash_password("password123"),
        full_name="Test User"
    )
    db.add(user)
    await db.commit()
    return user

@pytest_asyncio.fixture
async def auth_headers(test_user) -> dict:
    token = create_access_token(str(test_user.id))
    return {"Authorization": f"Bearer {token}"}