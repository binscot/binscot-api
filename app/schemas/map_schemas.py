from pydantic import BaseModel


class MapData(BaseModel):
    city: str
    country_code: str
