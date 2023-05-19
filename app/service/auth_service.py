from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from jwt.exceptions import ExpiredSignatureError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud import user_crud
from app.database.database import get_db
from app.data_type.token_type import Token
from app.schemas.token_schemas import TokenData
from app.schemas.user_schemas import User

ALGORITHM = settings.HASH_ALGORITHM
JWT_SECRET_KEY = settings.JWT_SECRET_KEY
JWT_REFRESH_SECRET_KEY = settings.JWT_REFRESH_SECRET_KEY

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#1

def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_context.hash(password)


def authenticate_user(db, username: str, password: str):
    user = user_crud.get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_jwt_token(data: dict, token_type: Token):
    print(token_type)
    print(Token.get_key(token_type))
    if token_type is None:
        raise HTTPException(status_code=500, detail="token_type is None")
    else:
        expire = datetime.utcnow() + timedelta(minutes=Token.get_expire_minutes(token_type))
    to_encode = data.copy()

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Token.get_key(token_type), algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], token_type: Token,db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, Token.get_key(token_type), algorithms=[ALGORITHM])
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

