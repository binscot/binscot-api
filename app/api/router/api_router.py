from fastapi import APIRouter

from app.api.endpoints import post, user, auth

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(post.router, prefix="/posts", tags=["posts"])
