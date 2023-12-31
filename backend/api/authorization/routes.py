from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from api.authorization.utils import authenticate_user, create_access_token
from dependencies import get_db
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from schemas import Token
from settings import ACCESS_TOKEN_EXPIRE_MINUTES



authorization_router = APIRouter()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@authorization_router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)):
    user = authenticate_user(
        db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
