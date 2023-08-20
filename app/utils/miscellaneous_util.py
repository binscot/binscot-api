import re
import json

from datetime import datetime, timedelta

import requests

from app.core.config import settings

RANDOM_CAT_URL = settings.RANDOM_CAT_URL


def get_random_cat_image():
    response = requests.get(RANDOM_CAT_URL)
    data = response.json()

    if data:
        cat_image_url = data[0]['url']
        return cat_image_url
    else:
        return None


def byte_to_json_str(byte_str):
    try:
        decoded_string = byte_str.decode("utf-8")
        json_data = json.loads(decoded_string)
        return json.dumps(json_data)
    except Exception as e:
        print('byte_to_string error')
        return e


def read_html_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            return content
    except Exception as e:
        return e


def multiple_replace(text, replacements):
    pattern = re.compile("|".join(replacements.keys()))
    return pattern.sub(lambda m: replacements[m.group(0)], text)


def convert_temperature(kelvin: float):
    return round(kelvin - 273.15, 2)


def convert_unix_time(utc_time):
    try:
        utc_time = datetime.utcfromtimestamp(utc_time)
        kst_time = utc_time + timedelta(hours=9)
        korea_time_str = kst_time.strftime('%Y-%m-%d %H:%M:%S')
        return korea_time_str
    except Exception as e:
        return f"error: {str(e)}"
