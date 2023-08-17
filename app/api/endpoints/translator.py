from fastapi import APIRouter

from app.schemas import translator_schemas
from app.service import translator_service

router = APIRouter()


@router.post("/translation")
async def translate_text(
        translation_data: translator_schemas.TranslationData
):
    return await translator_service.translate_text(translation_data)


@router.get("/sensing")
async def detect_language(
        sensing_data: translator_schemas.SensingData
):
    return await translator_service.detect_language(sensing_data)
