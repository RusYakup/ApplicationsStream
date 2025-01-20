import pytest_asyncio
from sqlalchemy import text
from src.config import Settings
from src.modeldb import DatabaseManager, Application


@pytest_asyncio.fixture
async def clean_db(db_manager):
    async with db_manager.engine.begin() as conn:
        await conn.execute(text("TRUNCATE TABLE applications RESTART IDENTITY"))
    yield
    async with db_manager.engine.begin() as conn:
        await conn.execute(text("TRUNCATE TABLE applications RESTART IDENTITY"))


@pytest_asyncio.fixture
async def db_manager():
    return DatabaseManager(Settings())


@pytest_asyncio.fixture
async def application():
    return Application(user_name="test_user", description="test_description")