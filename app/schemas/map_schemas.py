from pydantic import BaseModel, field_validator


class MapData(BaseModel):
    city: str
    country_code: str

    @field_validator('city', 'country_code')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError(v, '빈 값은 허용되지 않습니다.')
        return v
