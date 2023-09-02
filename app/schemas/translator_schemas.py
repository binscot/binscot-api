from pydantic import BaseModel, field_validator


class TranslationData(BaseModel):
    text: str
    source_lang: str
    target_lang: str

    @field_validator('text', 'source_lang', 'target_lang')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v


class SensingData(BaseModel):
    text: str

    @field_validator('text')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v


class TranslationResDTO(BaseModel):
    source_lang: str
    target_lang: str
    translated_text: str


class TranslationReqData(BaseModel):
    text: str
    source_lang: str
    target_lang: str

    @field_validator('text', 'source_lang', 'target_lang')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v


class SensingResDTO(BaseModel):
    detected_language: str


class SensingReqData(BaseModel):
    text: str

    @field_validator('text')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v
