import os
from os import path

from dotenv import load_dotenv
from pydantic import BaseSettings

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
load_dotenv()


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY')
    JWT_REFRESH_SECRET_KEY: str = os.getenv('JWT_REFRESH_SECRET_KEY')
    HASH_ALGORITHM: str = os.getenv('HASH_ALGORITHM')
    SQLALCHEMY_DATABASE_URL: str = os.getenv('SQLALCHEMY_DATABASE_URL')
    SQLALCHEMY_TEST_DATABASE_URL: str = os.getenv('SQLALCHEMY_TEST_DATABASE_URL')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
    REFRESH_TOKEN_EXPIRE_MINUTES: int = os.getenv('REFRESH_TOKEN_EXPIRE_MINUTES')

    class Config:
        case_sensitive = True


settings = Settings()
