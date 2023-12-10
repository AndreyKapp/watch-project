from datetime import datetime, timedelta
from typing import Annotated, Union
from fastapi import Cookie, Depends, HTTPException, status

from passlib.context import CryptContext
from sqlalchemy.orm import Session
from pydantic import TypeAdapter
from fastapi.security import OAuth2PasswordBearer
from dependencies.db_session import get_db

from schemas import UserInDB
from settings import SECRET_KEY, ALGORITHM
from sql.crud import get_db_user
from jose import jwt, JWTError


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: Session, username: str):
    user = get_db_user(db, username)
    if user:
        return TypeAdapter(UserInDB).validate_python(user)


def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(
        data: dict, 
        expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
        db: Session = Depends(get_db),
        authorization: Annotated[str | None, Cookie()] = None):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = authorization.split(' ')[1] if authorization else None
    if not token:
        return
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        return
    user = get_user(db, username=username)
    if user is None:
        raise credentials_exception
    return user
