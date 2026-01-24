from typing import Annotated
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from .. import database, schemas, models, utils, oauth2

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", response_model=schemas.Token)
def login_user(
    user_creds: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: database.Session = Depends(database.get_db)
):
    user = db.query(models.User).filter(models.User.email == user_creds.username).first() # legit

    if user is None or not utils.verify_password(user_creds.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = oauth2.create_access_token(
        data={"user_id": user.id},
        expires_delta=timedelta(minutes=oauth2.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return schemas.Token(access_token=access_token, token_type="bearer")
