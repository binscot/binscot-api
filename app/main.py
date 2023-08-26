from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI

from fastapi.exceptions import RequestValidationError

from app.api.router.api_router import api_router
from app.core import config
from app.database.database import engine
from app.handlers.exception_handlers import validation_exception_handler
from app.middleware.api_middleware import api_request_middleware
from app.models import models
from app.service import server_state_service


models.Base.metadata.create_all(bind=engine)

config.setup_logging()

app = FastAPI()
app.include_router(api_router, prefix=config.settings.API_V1_STR)
app.middleware("http")(api_request_middleware)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(server_state_service.send_server_state, trigger="cron", hour=6, minute=0)

