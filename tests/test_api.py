import pytest
from httpx import ASGITransport, AsyncClient
from src.handlers import app
from tests.conftest import db_manager, clean_db


@pytest.mark.asyncio
async def test_endpoints(clean_db, db_manager):
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://localhost:8000"
    ) as ac:
        application_in = {"user_name": "test_name", "description": "test_description"}
        # Create record
        response = await ac.post("/applications", json=application_in)
        assert response.status_code == 201
        assert response.json() == {"message": "Application created successfully"}
        # Check that records exists
        response = await ac.get("/applications")
        assert response.status_code == 200
        assert response.json()["applications"][0]["user_name"] == application_in["user_name"]
        assert response.json()["applications"][0]["description"] == application_in["description"]