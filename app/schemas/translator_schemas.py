from pydantic import BaseModel


class TranslationRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str


class TranslationResponse(BaseModel):
    source_lang: str
    target_lang: str
    translated_text: str
