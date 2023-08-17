from datetime import datetime, timedelta

import requests

from app.core.config import settings

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
            dt = item.get("dt")
            humidity = item.get("main", {}).get("humidity")
            weather_list = item.get("weather", [])
            if weather_list:
                weather_main = weather_list[0].get("main")
                weather_description = weather_list[0].get("description")
            pop = item.get("pop")

            utc_time = datetime.utcfromtimestamp(dt)
            kst_time = utc_time + timedelta(hours=9)

            result.append({
                "dt": kst_time.strftime('%Y-%m-%d %H:%M:%S'),
                "humidity": humidity,
                "weather_main": weather_main,
                "weather_description": weather_description,
                "pop": pop
            })

    return result


def get_weather_now(map_data):
    data = get_weather_data_json(
        map_data,
        OPENWEATHERMAP_WEATHER_TODAY_URL
    )
    if data.get("cod") == 200:
        utc_time = datetime.utcfromtimestamp(data.get("dt"))
        kst_time = utc_time + timedelta(hours=9)
        transformed_data = {
            "dt": kst_time.strftime('%H:%M:%S'),
            "weather": data.get("weather")[0]["main"],
            "weather_description": data.get("weather")[0]["description"],
            "humidity": data.get("main")["humidity"]
        }
        return transformed_data


def get_weather_data_json(
        map_data,
        url
):
    params = {
        "q": f"{map_data.city},{map_data.country_code}",
        "appid": OPENWEATHERMAP_API_KEY,
    }

    return requests.get(url, params=params).json()
