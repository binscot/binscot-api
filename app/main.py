from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
#####################
from fastapi import WebSocket, Request
from fastapi.exceptions import RequestValidationError
from starlette.templating import Jinja2Templates

from app.api.router.api_router import api_router
from app.core import config
from app.database.database import engine
from app.handlers.exception_handlers import validation_exception_handler
from app.middleware.api_middleware import api_request_middleware
from app.models import models
from app.service import server_state_service

###################

models.Base.metadata.create_all(bind=engine)

config.setup_logging()

app = FastAPI()
app.include_router(api_router, prefix=config.settings.API_V1_STR)
app.middleware("http")(api_request_middleware)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(server_state_service.send_server_state, trigger="cron", hour=6, minute=0)

#####################


chat_messages = []

templates = Jinja2Templates(directory="resource/templates")


@app.get("/chat")
async def client(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            print(data)
            chat_messages.append(data)
            await websocket.send_text(data)
            if data == "/close":
                await websocket.close(code=1000, reason="User has closed the connection")
        except Exception as e:
            print(e)
            await websocket.close()
