import httpx
from app.dto.response_dto import TranslationResDTO, SensingResDTO, BaseResponseDTO
from app.core.config import settings

PAPAGO_CLIENT_ID = settings.NAVER_CLIENT_ID
PAPAGO_CLIENT_SECRET = settings.NAVER_CLIENT_SECRET
PAPAGO_URL = settings.PAPAGO_URL
PAPAGO_DETECT_LANGUAGE_URL = settings.PAPAGO_DETECT_LANGUAGE_URL


async def translate_text(translation_data):
    text = translation_data.text
    source_lang = translation_data.source_lang
    target_lang = translation_data.target_lang

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
            response_data = TranslationResDTO(source_lang=source_lang, target_lang=target_lang,
                                              translated_text=translated_text)
            return BaseResponseDTO(
                status_code=200,
                data=response_data.__dict__,
                detail='success'
            )
        else:
            return BaseResponseDTO(
                status_code=500,
                data=None,
                detail='Translation failed.'
            )


async def detect_language(sensing_data):
    headers = {
        "X-Naver-Client-Id": PAPAGO_CLIENT_ID,
        "X-Naver-Client-Secret": PAPAGO_CLIENT_SECRET
    }

    params = {"query": sensing_data.text}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(PAPAGO_DETECT_LANGUAGE_URL, headers=headers, data=params)
            response.raise_for_status()
            result = response.json()

            if "langCode" in result:
                response_data = SensingResDTO(detected_language=result["langCode"])
                return BaseResponseDTO(
                    status_code=200,
                    data=response_data.__dict__,
                    detail='success'
                )
            else:
                return BaseResponseDTO(
                    status_code=500,
                    data=None,
                    detail='Failed to detect language'
                )
        except httpx.RequestError as e:
            return BaseResponseDTO(
                status_code=500,
                data=None,
                detail=str(e)
            )
