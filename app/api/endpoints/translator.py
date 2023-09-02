from fastapi import APIRouter

from app.schemas.translator_schemas import TranslationReqData, SensingReqData
from app.service import translator_service
from app.dto.response_dto import BaseResponseDTO
router = APIRouter()


@router.post("/translation", response_model=BaseResponseDTO)
async def translate_text(translation_data: TranslationReqData):
    return await translator_service.translate_text(translation_data)


@router.get("/sensing", response_model=BaseResponseDTO)
async def detect_language(sensing_data: SensingReqData):
    return await translator_service.detect_language(sensing_data)
