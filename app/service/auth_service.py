from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse

from jose import JWTError, jwt
from jwt.exceptions import ExpiredSignatureError

from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud import user_crud
from app.data_type.token_type import Token
from app.database.database import get_db
from app.schemas import token_schemas
from app.schemas import user_schemas
from app.schemas.user_schemas import User
from app.core import consts

ALGORITHM = settings.HASH_ALGORITHM
JWT_SECRET_KEY = settings.JWT_SECRET_KEY
JWT_REFRESH_SECRET_KEY = settings.JWT_REFRESH_SECRET_KEY


# 1
def create_access_token(db, request):
    user = verify_token(request.cookies.get(Token.REFRESH_TOKEN), Token.get_key(Token.REFRESH_TOKEN),
                        settings.HASH_ALGORITHM, db)
    access_token = create_jwt_token(data={"sub": user.username}, token_type=Token.ACCESS_TOKEN)
    return token_schemas.Token(access_token=access_token, token_type="bearer", username=user.username)


def login(db, form_data):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_jwt_token(data={"sub": user.username}, token_type=Token.ACCESS_TOKEN)
    refresh_token = create_jwt_token(data={"sub": user.username}, token_type=Token.REFRESH_TOKEN)

    response = JSONResponse(
        content=token_schemas.Token(access_token=access_token, token_type="bearer", username=user.username).__dict__)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
    return response


def create_user(db, user: user_schemas.UserCreate):
    UserInDB = user_crud.get_user_by_username(db, username=user.username)
    if UserInDB:
        raise HTTPException(status_code=400, detail="username already registered")
    user = user_crud.create_user(db=db, user=user)
    return user_schemas.User(id=user.id, username=user.username, disabled=user.disabled, posts=user.posts)


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


def create_jwt_token(data: dict, token_type: Token):
    if token_type is None:
        raise HTTPException(status_code=500, detail="token_type is None")
    else:
        expire = datetime.utcnow() + timedelta(minutes=Token.get_expire_minutes(token_type))
    to_encode = data.copy()

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Token.get_key(token_type), algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(consts.oauth2_scheme)],
                           db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, Token.get_key(Token.ACCESS_TOKEN), algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = token_schemas.TokenData(username=username)
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
