import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_get_weather():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.post(
            "/api/weather",
            json={
                "latitude": 52.52,
                "longitude": 13.41,
                "hourly": "temperature_2m",
                "timezone": "Europe/Berlin"
            }
        )
    assert response.status_code == 200
    data = response.json()
    assert "latitude" in data
    assert data["latitude"] == 52.52
    assert "longitude" in data
    assert data["longitude"] == 13.41
    assert "hourly_data" in data
    assert "temperature_2m" in data["hourly_data"]

@pytest.mark.asyncio
async def test_get_weather_graph():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.get(
            "/api/weather/graph",
            params={"latitude": 52.52, "longitude": 13.41, "timezone": "Europe/Berlin"}
        )
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
