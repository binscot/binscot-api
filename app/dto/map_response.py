from pydantic import BaseModel


class MapResponseDTO(BaseModel):
    city: str
    country: str
    lat: float
    lon: float
