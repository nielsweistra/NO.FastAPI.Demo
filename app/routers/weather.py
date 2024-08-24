from fastapi import APIRouter, Query, HTTPException, Depends
from fastapi.responses import StreamingResponse
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import io
import matplotlib.pyplot as plt
from models.weather import WeatherRequest, WeatherResponse

router = APIRouter()

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)


@router.post("/weather", response_model=WeatherResponse, tags=["weather"])
async def get_weather(request: WeatherRequest):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": request.latitude,
        "longitude": request.longitude,
        "hourly": request.hourly,
        "timezone": request.timezone,
    }

    try:
        responses = openmeteo.weather_api(url, params=params)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not responses:
        raise HTTPException(status_code=404, detail="No data found")

    response = responses[0]
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left",
        ).tolist(),
        "temperature_2m": hourly_temperature_2m.tolist(),
    }

    weather_response = WeatherResponse(
        latitude=response.Latitude(),
        longitude=response.Longitude(),
        elevation=response.Elevation(),
        timezone=response.Timezone(),
        timezone_abbreviation=response.TimezoneAbbreviation(),
        utc_offset_seconds=response.UtcOffsetSeconds(),
        hourly_data=hourly_data,
    )

    return weather_response


@router.get("/weather/graph", tags=["weather"])
async def get_weather_graph(
    latitude: float = Query(...),
    longitude: float = Query(...),
    timezone: str = Query("Europe/Berlin"),
):
    weather_request = WeatherRequest(
        latitude=latitude, longitude=longitude, timezone=timezone
    )
    weather_data = await get_weather(weather_request)

    plt.figure(figsize=(10, 6))
    plt.plot(
        weather_data.hourly_data["date"],
        weather_data.hourly_data["temperature_2m"],
        label="Temperature (2m)",
    )
    plt.xlabel("Time")
    plt.ylabel("Temperature (°C)")
    plt.title(f"Temperature Over Time at ({latitude}, {longitude})")
    plt.legend()
    plt.grid(True)

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()

    return StreamingResponse(buf, media_type="image/png")
