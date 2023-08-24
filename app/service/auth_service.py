from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from jwt.exceptions import ExpiredSignatureError
from sqlalchemy.orm import Session

from app.core import consts
from app.core.config import settings
from app.crud import user_crud
from app.data_type.token_type import TokenType
from app.database.database import get_db
from app.dto.base_response_dto import BaseResponseDTO
from app.schemas.token_schemas import Token, TokenData
from app.schemas.user_schemas import User

ALGORITHM = settings.HASH_ALGORITHM


# 1
def create_access_token(db, request):
    refresh_token = request.cookies.get(TokenType.REFRESH_TOKEN)
    if refresh_token is None:
        return BaseResponseDTO(
            status_code=401,
            data=None,
            detail='refresh_token is None'
        )
    user = verify_token(
        refresh_token,
        TokenType.get_key(TokenType.REFRESH_TOKEN),
        settings.HASH_ALGORITHM, db
    )
    access_token = create_jwt_token(data={"sub": user.username}, token_type=TokenType.ACCESS_TOKEN)
    response_data = Token(access_token=access_token, token_type="bearer", username=user.username)
    return BaseResponseDTO(
        status_code=200,
        data=response_data.__dict__,
        detail='success'
    )


def login(db, form_data, response):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        return BaseResponseDTO(
            status_code=401,
            data=None,
            detail='Incorrect username or password'
        )
    response_data = Token(
        access_token=create_jwt_token(data={"sub": user.username}, token_type=TokenType.ACCESS_TOKEN),
        token_type="bearer",
        username=user.username
    )
    response.set_cookie(
        key="refresh_token",
        value=create_jwt_token(data={"sub": user.username}, token_type=TokenType.REFRESH_TOKEN), httponly=True)
    return BaseResponseDTO(
        status_code=200,
        data=response_data.__dict__,
        detail='success'
    )


def create_user(db, user):
    UserInDB = user_crud.get_user_by_username(db, username=user.username)
    if UserInDB:
        print(12)
        return BaseResponseDTO(
            status_code=400,
            data=None,
            detail='username already registered'
        )
    user = user_crud.create_user(db=db, user=user)
    response_data = User(id=user.id, username=user.username, disabled=user.disabled, posts=user.posts)
    return BaseResponseDTO(
        status_code=200,
        data=response_data.__dict__,
        detail='success'
    )


def verify_password(plain_password, hashed_password):
    return consts.password_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return consts.password_context.hash(password)


def authenticate_user(db, username: str, password: str):
    user = user_crud.get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_jwt_token(data: dict, token_type: TokenType):
    if token_type is None:
        raise HTTPException(status_code=500, detail="token_type is None")
    else:
        expire = datetime.utcnow() + timedelta(minutes=TokenType.get_expire_minutes(token_type))
    to_encode = data.copy()

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, TokenType.get_key(token_type), algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(consts.oauth2_scheme)],
                           db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, TokenType.get_key(TokenType.ACCESS_TOKEN), algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = user_crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def verify_token(token: str, secret_key: str, algorithm: str, db: Session):
    try:
        payload = jwt.decode(token, secret_key, algorithm)
        username = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = user_crud.get_user_by_username(db, username=username)

        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
