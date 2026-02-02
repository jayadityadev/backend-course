from typing import Annotated
import jwt
from datetime import datetime, timedelta, timezone
from pydantic import ValidationError
from sqlalchemy.orm import Session
from . import models, database, exceptions, config, schemas
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

# openssl rand -hex 32
SECRET_KEY = config.settings.jwt_secret_key
ALGORITHM = config.settings.jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = config.settings.jwt_expire_time

# Token created
def create_access_token(data: schemas.TokenData, expires_delta: timedelta | None = None):
    to_encode = data.model_copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.exp = expire
    encoded_jwt = jwt.encode(to_encode.model_dump(), SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Decode the received token, verify it, and return the current user
def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Annotated[Session, Depends(database.get_db)]
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = schemas.TokenData(**payload)
    except (jwt.PyJWTError, ValidationError):
        raise exceptions.credentials_exception
    if token_data.sub is None:
        raise exceptions.credentials_exception
    try:
        user_id = int(token_data.sub)
    except ValueError:
        raise exceptions.credentials_exception
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise exceptions.credentials_exception
    return user
