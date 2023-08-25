from typing import List, Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud import user_crud
from app.database.database import get_db
from app.schemas import user_schemas
from app.service import auth_service

router = APIRouter()


@router.get("/", response_model=List[user_schemas.User])
def read_users(db: Session = Depends(get_db)):
    users = user_crud.get_users(db)
    return users


@router.get("/me", response_model=user_schemas.User)
async def read_users_me(
        current_user: Annotated[user_schemas.User, Depends(auth_service.get_current_active_user)]
):
    return current_user
