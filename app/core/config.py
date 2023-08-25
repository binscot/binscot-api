import os
from os import path
import logging
from dotenv import load_dotenv
from pydantic import EmailStr
from pydantic_settings import BaseSettings

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
load_dotenv()


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"

    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY')
    JWT_REFRESH_SECRET_KEY: str = os.getenv('JWT_REFRESH_SECRET_KEY')
    HASH_ALGORITHM: str = os.getenv('HASH_ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
    REFRESH_TOKEN_EXPIRE_MINUTES: int = os.getenv('REFRESH_TOKEN_EXPIRE_MINUTES')

    SQLALCHEMY_DATABASE_URL: str = os.getenv('SQLALCHEMY_DATABASE_URL')

    NAVER_CLIENT_ID: str = os.getenv('NAVER_CLIENT_ID')
    NAVER_CLIENT_SECRET: str = os.getenv('NAVER_CLIENT_SECRET')
    PAPAGO_URL: str = os.getenv('PAPAGO_URL')
    PAPAGO_DETECT_LANGUAGE_URL: str = os.getenv('PAPAGO_DETECT_LANGUAGE_URL')

    KAKAO_TOKEN_URL: str = os.getenv('KAKAO_TOKEN_URL')
    KAKAO_SEND_URL: str = os.getenv('KAKAO_SEND_URL')
    KAKAO_CLIENT_ID: str = os.getenv('KAKAO_CLIENT_ID')

    RANDOM_CAT_URL: str = os.getenv('RANDOM_CAT_URL')

    OPENWEATHERMAP_API_KEY: str = os.getenv('OPENWEATHERMAP_API_KEY')
    OPENWEATHERMAP_LOCATION_URL: str = os.getenv('OPENWEATHERMAP_LOCATION_URL')
    OPENWEATHERMAP_WEATHER_WEEK_URL: str = os.getenv('OPENWEATHERMAP_WEATHER_WEEK_URL')
    OPENWEATHERMAP_WEATHER_TODAY_URL: str = os.getenv('OPENWEATHERMAP_WEATHER_TODAY_URL')

    SMTP_SERVER: str = os.getenv('SMTP_SERVER')
    SMTP_PORT: int = os.getenv('SMTP_PORT')
    SMTP_USERNAME: str = os.getenv('SMTP_USERNAME')
    SMTP_PASSWORD: str = os.getenv('SMTP_PASSWORD')
    OWNER_MAIL: EmailStr = os.getenv('OWNER_MAIL')

    REDIS_SERVER: str = os.getenv('REDIS_SERVER')
    REDIS_PORT: int = os.getenv('REDIS_PORT')
    REDIS_DB: int = os.getenv('REDIS_DB')
    REDIS_PASSWORD: str = os.getenv('REDIS_PASSWORD')

    class Config:
        case_sensitive = True


settings = Settings()


def setup_logging():
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(name)s][%(levelname)s][%(message)s]')
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.handlers = logging.getLogger().handlers
