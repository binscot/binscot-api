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
