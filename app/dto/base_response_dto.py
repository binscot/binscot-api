from typing import Optional

from pydantic import BaseModel


class BaseResponseDTO(BaseModel):
    status_code: int
    data: Optional[dict] = None
    detail: str

    class Config:
        validate_assignment = True
