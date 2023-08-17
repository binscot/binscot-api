from typing import List, Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud import user_crud
from app.database.database import get_db
from app.schemas.user_schemas import User
from app.service.auth_service import get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[User])
def read_users(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    users = user_crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/me", response_model=User)
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user
