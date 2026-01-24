from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .database import get_db
from . import oauth2, models

DBSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[models.User, Depends(oauth2.get_current_user)]
PasswordRequestForm = Annotated[OAuth2PasswordRequestForm, Depends()]
