import logging

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class CredentialsException(Exception):
    def __init__(self, name: str):
        self.name = name


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_messages = [
        f"Field '{', '.join(error['loc'])}': {error['msg']}"
        for error in exc.errors()
    ]

    logging.error(error_messages)
    response_content = {
        "status_code": 400,
        "detail": "Validation error",
        "errors": error_messages,
        "original_request": {
            "client": request.client,
            "url": str(request.url)
        }
    }

    return JSONResponse(content=response_content, status_code=400)


async def credentials_exception_handler(request: Request, exc: CredentialsException):
    response_content = {
        'status_code': 401,
        'detail': 'Could not validate credentials',
        'errors': exc.name,
        'original_request': {
            'client': request.client,
            'url': str(request.url)
        }
    }

    return JSONResponse(content=response_content, status_code=400)
