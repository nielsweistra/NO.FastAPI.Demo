import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_get_weather_graph():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.get(
            "/api/weather/graph",
            params={"latitude": 52.52, "longitude": 13.41, "timezone": "Europe/Berlin"}
        )
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
