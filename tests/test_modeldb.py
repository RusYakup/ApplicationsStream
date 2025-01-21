import pytest
from sqlalchemy import select
from src.modeldb import Application
from tests.conftest import db_manager, application


@pytest.mark.asyncio
async def test_add_applications(db_manager, application, clean_db):
    await db_manager.add_application(application)
    async with db_manager.engine.begin() as conn:
        query = select(Application).where(Application.user_name == application.user_name)
        result = await conn.execute(query)
        apps = result.fetchall()
        assert len(apps) == 1
        assert apps[0].user_name == application.user_name
        assert apps[0].description == application.description


@pytest.mark.asyncio
async def test_get_applications(db_manager, application, clean_db):
    await db_manager.add_application(application)
    result = await db_manager.get_applications(application.user_name)
    app = result[0]
    assert app.id is not None
    assert app.user_name == application.user_name
    assert app.description == application.description
