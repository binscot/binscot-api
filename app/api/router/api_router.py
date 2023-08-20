from fastapi import APIRouter

from app.api.endpoints import post, user, auth, translator, map, weather, kakao, mail, test, chat

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(post.router, prefix="/posts", tags=["posts"])
api_router.include_router(translator.router, prefix="/translator", tags=["translator"])
api_router.include_router(map.router, prefix="/map", tags=["map"])
api_router.include_router(weather.router, prefix="/weather", tags=["weather"])
api_router.include_router(kakao.router, prefix="/kakao", tags=["kakao"])
api_router.include_router(mail.router, prefix="/mail", tags=["mail"])
api_router.include_router(test.router, prefix="/test", tags=["test"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
