import asyncio
import os
from typing import Generator, Any

import asyncpg
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

import settings
from db.session import get_db
from main import app

# create async engine for interaction with database
test_engine = create_async_engine(settings.TEST_DATABASE_URL, future=True, echo=True)

# create session for the interaction with database
test_async_session = sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)

CLEAN_TABLES = [
    "users",
]


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session', autouse=True)
async def run_migrations():
    os.system('alembic init migrations')
    os.system('alembic revision --autogenerate -m "test running migrations"')
    os.system('alembic upgrade heads')


@pytest.fixture(scope='session')
async def async_session_test():
    engine = create_async_engine(settings.TEST_DATABASE_URL, future=True, echo=True)
    async_session = sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)
    yield async_session


@pytest.fixture(scope="function", autouse=True)
async def clean_tables(async_session_test):
    async with async_session_test() as session:
        async with session.begin():
            for table_for_cleaning in CLEAN_TABLES:
                await session.execute(f"""TRUNCATE TABLE {table_for_cleaning};""")


@pytest.fixture(scope="function")
async def client() -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that use the 'db_session' fixture to override
    the 'get_db' dependency that is injected into routes
    """
    async def _get_test_db():
        try:
            yield test_async_session()
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
async def async_pgpool():
    pool = await asyncpg.create_pool("".join(settings.TEST_DATABASE_URL.split("+asyncpg")))
    yield pool
    pool.close()


@pytest.fixture
async def get_user_from_database(async_pgpool):
    
    async def get_user_from_database_by_uuid(user_id: str):
        async with async_pgpool.acquire() as connection:
            return await connection.fetch(f"""SELECT * FROM users WHERE user_id = {user_id};""")

    return get_user_from_database_by_uuid