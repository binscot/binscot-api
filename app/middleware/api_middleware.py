import logging

from fastapi import Request


def api_request_middleware(request: Request, call_next):
    log_msg = f"API Request - {request.method} {request.url.path} - {request.client.host}"
    logging.info(log_msg)
    response = call_next(request)
    return response
