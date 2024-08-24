from pydantic import BaseModel

class WeatherRequest(BaseModel):
    latitude: float
    longitude: float
    hourly: str = "temperature_2m"
    timezone: str = "Europe/Berlin"

class WeatherResponse(BaseModel):
    latitude: float
    longitude: float
    elevation: float
    timezone: str
    timezone_abbreviation: str
    utc_offset_seconds: int
    hourly_data: dict
