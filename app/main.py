from fastapi import FastAPI
import logging
from app.api.router.api_router import api_router
from app.core.config import settings
from app.database.database import engine
from app.models import models
from apscheduler.schedulers.background import BackgroundScheduler
from app.service import kakao_service

logging.basicConfig(level=logging.INFO)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(api_router, prefix=settings.API_V1_STR)

# scheduler = BackgroundScheduler()
# scheduler.start()
# scheduler.add_job(kakao_service.send_server_state_kakao_message, trigger="cron", hour=6, minute=0)
