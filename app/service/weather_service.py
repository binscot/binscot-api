from datetime import datetime

import requests

from app.core.config import settings
from app.schemas import weather_schemas
from app.utils import miscellaneous_util

OPENWEATHERMAP_API_KEY = settings.OPENWEATHERMAP_API_KEY
OPENWEATHERMAP_WEATHER_WEEK_URL = settings.OPENWEATHERMAP_WEATHER_WEEK_URL
OPENWEATHERMAP_WEATHER_TODAY_URL = settings.OPENWEATHERMAP_WEATHER_TODAY_URL


def get_weather_week(map_data):
    data = get_weather_data_json(
        map_data,
        OPENWEATHERMAP_WEATHER_WEEK_URL
    )

    result = []
    if data.get("cod") == "200":
        for item in data.get("list", []):
            weather = item.get("weather", [])[0]

            try:
                kst_time = miscellaneous_util.convert_unix_time(item.get("dt"))
                celsius = miscellaneous_util.convert_temperature(item.get("main", {}).get("temp"))
                feels_like = miscellaneous_util.convert_temperature(item.get("main", {}).get("feels_like"))
                celsius_min = miscellaneous_util.convert_temperature(item.get("main", {}).get("temp_min"))
                celsius_max = miscellaneous_util.convert_temperature(item.get("main", {}).get("temp_max"))
                icon = weather.get("icon")
                wind = item.get("wind", {}).get("speed")
                humidity = item.get("main", {}).get("humidity")
                weather_main = weather.get("main")
                description = weather.get("description")
                probability_of_precipitation = int(item.get("pop")) * 100
                last_rain_3h = item.get("rain", {}).get("3h")
                last_snow_3h = item.get("snow", {}).get("3h")

                if last_rain_3h is not None:
                    last_rain_3h = f"{last_rain_3h}mm"

                if last_snow_3h is not None:
                    last_snow_3h = f"{last_snow_3h}mm"

                weather_item = weather_schemas.WeatherWeek(
                    kst_time=kst_time,
                    celsius=celsius,
                    feels_like=feels_like,
                    celsius_min=celsius_min,
                    celsius_max=celsius_max,
                    icon=icon,
                    wind=str(wind) + 'm/s',
                    last_rain_3h=last_rain_3h,
                    last_snow_3h=last_snow_3h,
                    humidity=str(humidity) + '%',
                    weather_main=weather_main,
                    weather_description=description,
                    pop=str(probability_of_precipitation) + '%'
                )
                result.append(weather_item)
            except Exception as e:
                return e

    return weather_schemas.WeatherWeekList(data=result)


def get_weather_now(map_data):
    data = get_weather_data_json(
        map_data,
        OPENWEATHERMAP_WEATHER_TODAY_URL
    )

    try:
        if data.get("cod") == 200:
            weather = data.get("weather", [])[0]

            kst_time = datetime.now()
            lon = data.get("coord", {}).get("lon")
            lat = data.get("coord", {}).get("lat")
            weather_main = weather.get("main")
            description = weather.get("description")
            icon = weather.get("icon")
            celsius = miscellaneous_util.convert_temperature(data.get("main", {}).get("temp"))
            feels_like = miscellaneous_util.convert_temperature(data.get("main", {}).get("feels_like"))
            celsius_min = miscellaneous_util.convert_temperature(data.get("main", {}).get("temp_min"))
            celsius_max = miscellaneous_util.convert_temperature(data.get("main", {}).get("temp_max"))
            humidity = data.get("main", {}).get("humidity")
            wind = data.get("wind", {}).get("speed")

            sunrise = miscellaneous_util.convert_unix_time(data.get("sys", {}).get("sunrise"))
            sunset = miscellaneous_util.convert_unix_time(data.get("sys", {}).get("sunset"))
            country = data.get("sys", {}).get("country")
            city = data.get("name")

            last_rain_3h = data.get("rain", {}).get("3h")
            last_rain_1h = data.get("rain", {}).get("1h")
            last_snow_3h = data.get("snow", {}).get("3h")
            last_snow_1h = data.get("snow", {}).get("1h")

            return weather_schemas.WeatherNow(
                kst_time=kst_time,
                country=country,
                city=city,
                lon=lon,
                lat=lat,
                weather_main=weather_main,
                description=description,
                icon=icon,
                last_rain_3h=f"{last_rain_3h}mm" if last_rain_3h is not None else None,
                last_rain_1h=f"{last_rain_1h}mm" if last_rain_1h is not None else None,
                last_snow_3h=f"{last_snow_3h}mm" if last_snow_3h is not None else None,
                last_snow_1h=f"{last_snow_1h}mm" if last_snow_1h is not None else None,
                celsius=celsius,
                feels_like=feels_like,
                celsius_min=celsius_min,
                celsius_max=celsius_max,
                humidity=str(humidity) + '%',
                wind=str(wind) + 'm/s',
                sunrise=sunrise,
                sunset=sunset
            )
    except Exception as e:
        return e


def get_weather_data_json(
        map_data,
        url
):
    params = {
        "q": f"{map_data.city},{map_data.country_code}",
        "appid": OPENWEATHERMAP_API_KEY,
    }

    return requests.get(url, params=params).json()
