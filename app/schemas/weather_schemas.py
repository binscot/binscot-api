from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class WeatherNow(BaseModel):
    kst_time: datetime
    city: str
    country: str
    lon: Optional[float]
    lat: Optional[float]
    weather_main: str
    description: str
    icon: str
    last_rain_3h: Optional[str]
    last_rain_1h: Optional[str]
    last_snow_3h: Optional[str]
    last_snow_1h: Optional[str]
    celsius: float
    feels_like: float
    celsius_min: float
    celsius_max: float
    humidity: str
    wind: str
    sunrise: datetime
    sunset: datetime


class WeatherWeek(BaseModel):
    kst_time: datetime
    celsius: float
    feels_like: float
    celsius_min: float
    celsius_max: float
    icon: str
    wind: str
    last_rain_3h: Optional[str]
    last_snow_3h: Optional[str]
    humidity: str
    weather_main: str
    weather_description: str
    pop: str


class WeatherWeekList(BaseModel):
    data: List[WeatherWeek]
