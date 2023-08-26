from enum import StrEnum
from app.core.config import settings


class TokenType(StrEnum):
    ACCESS_TOKEN = "access_token"
    REFRESH_TOKEN = "refresh_token"

    def get_key(self):
        if self == "access_token":
            return settings.JWT_SECRET_KEY
        if self == "refresh_token":
            return settings.JWT_REFRESH_SECRET_KEY

    def get_expire_minutes(self):
        if self == "access_token":
            return settings.ACCESS_TOKEN_EXPIRE_MINUTES
        if self == "refresh_token":
            return settings.REFRESH_TOKEN_EXPIRE_MINUTES
