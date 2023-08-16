from fastapi import APIRouter, Query

from app.core.config import settings
from app.schemas.translator_schemas import TranslationRequest
from app.service import translator_service

router = APIRouter()

PAPAGO_CLIENT_ID = settings.NAVER_CLIENT_ID
PAPAGO_CLIENT_SECRET = settings.NAVER_CLIENT_SECRET
PAPAGO_URL = settings.PAPAGO_URL
PAPAGO_DETECT_LANGUAGE_URL = settings.PAPAGO_DETECT_LANGUAGE_URL


@router.post("/translatorText")
async def translate_text(request: TranslationRequest):
    return await translator_service.translate_text(request)


@router.get("/detectLanguage")
async def detect_language(text: str = Query(..., title="Text to detect language")):
    return await translator_service.detect_language(text=text)
