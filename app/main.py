from typing import Union
from fastapi import FastAPI, Query, HTTPException, APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import io
import matplotlib.pyplot as plt  # Importing Matplotlib
import requests
from bs4 import BeautifulSoup
import json


router = APIRouter(prefix='/api')

# Initialize the FastAPI app
app = FastAPI()


@router.get("/", tags=["default"])
def read_root():
    return {"Hello": "World"}

@router.get("/items/{item_id}", tags=["default"])
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Define request model for weather API
class WeatherRequest(BaseModel):
    latitude: float
    longitude: float
    hourly: str = "temperature_2m"
    timezone: str = "Europe/Berlin"

# Define response model for weather API
class WeatherResponse(BaseModel):
    latitude: float
    longitude: float
    elevation: float
    timezone: str
    timezone_abbreviation: str
    utc_offset_seconds: int
    hourly_data: dict

# New API endpoint to get weather data
@router.post("/weather", response_model=WeatherResponse, tags=["weather"])
async def get_weather(request: WeatherRequest):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": request.latitude,
        "longitude": request.longitude,
        "hourly": request.hourly,
        "timezone": request.timezone
    }

    try:
        responses = openmeteo.weather_api(url, params=params)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not responses:
        raise HTTPException(status_code=404, detail="No data found")

    # Process the first location response
    response = responses[0]

    # Extract hourly data
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        ).tolist(),
        "temperature_2m": hourly_temperature_2m.tolist()
    }

    # Prepare the response
    weather_response = WeatherResponse(
        latitude=response.Latitude(),
        longitude=response.Longitude(),
        elevation=response.Elevation(),
        timezone=response.Timezone(),
        timezone_abbreviation=response.TimezoneAbbreviation(),
        utc_offset_seconds=response.UtcOffsetSeconds(),
        hourly_data=hourly_data
    )

    return weather_response

# New API endpoint to create and return a temperature graph
@router.get("/weather/graph", tags=["weather"])
async def get_weather_graph(
    latitude: float = Query("52.377956"),
    longitude: float = Query("4.897070"),
    timezone: str = Query("Europe/Berlin")
):
    # Get the weather data
    weather_request = WeatherRequest(latitude=latitude, longitude=longitude, timezone=timezone)
    weather_data = await get_weather(weather_request)
    
    # Create a line plot using Matplotlib
    plt.figure(figsize=(10, 6))
    plt.plot(weather_data.hourly_data["date"], weather_data.hourly_data["temperature_2m"], label="Temperature (2m)")
    plt.xlabel("Time")
    plt.ylabel("Temperature (°C)")
    plt.title(f"Temperature Over Time at ({latitude}, {longitude})")
    plt.legend()
    plt.grid(True)

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    # Return the image as a StreamingResponse
    return StreamingResponse(buf, media_type="image/png")

app.include_router(router)