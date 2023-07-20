import httpx
from fastapi import APIRouter, HTTPException, Query
import requests

from app.schemas.translator_schemas import TranslationRequest, TranslationResponse
from app.core.config import settings

router = APIRouter()

PAPAGO_CLIENT_ID = settings.NAVER_CLIENT_ID
PAPAGO_CLIENT_SECRET = settings.NAVER_CLIENT_SECRET
PAPAGO_URL = "https://openapi.naver.com/v1/papago/n2mt"
PAPAGO_DETECT_LANGUAGE_URL = "https://openapi.naver.com/v1/papago/detectLangs"


@router.post("/translatorText", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    text = request.text
    source_lang = request.source_lang
    target_lang = request.target_lang

    if not text or not source_lang or not target_lang:
        raise HTTPException(status_code=400, detail="Text, source_lang, and target_lang are required.")

    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Naver-Client-Id": PAPAGO_CLIENT_ID,
        "X-Naver-Client-Secret": PAPAGO_CLIENT_SECRET,
    }

    data = {
        "source": source_lang,
        "target": target_lang,
        "text": text,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(PAPAGO_URL, data=data, headers=headers)

        if response.status_code == 200:
            result = response.json()
            translated_text = result['message']['result']['translatedText']
            return {"source_lang": source_lang, "target_lang": target_lang, "translated_text": translated_text}
        else:
            raise HTTPException(status_code=response.status_code, detail="Translation failed.")


@router.get("/detectLanguage")
async def detect_language(text: str = Query(..., title="Text to detect language")):
    headers = {
        "X-Naver-Client-Id": PAPAGO_CLIENT_ID,
        "X-Naver-Client-Secret": PAPAGO_CLIENT_SECRET
    }

    params = {"query": text}

    try:
        response = requests.post(PAPAGO_DETECT_LANGUAGE_URL, headers=headers, data=params)
        response.raise_for_status()
        result = response.json()
        if "langCode" in result:
            return {"detected_language": result["langCode"]}
        else:
            raise HTTPException(status_code=500, detail="Failed to detect language")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
