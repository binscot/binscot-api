from fastapi import FastAPI

from app.api.router.api_router import api_router
from app.core.config import settings
from app.database.database import engine
from app.models import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(api_router, prefix=settings.API_V1_STR)
