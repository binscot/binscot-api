import requests
import re
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