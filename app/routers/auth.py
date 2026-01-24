from datetime import timedelta
from fastapi import APIRouter, HTTPException, status
from .. import schemas, models, utils, deps, oauth2, exceptions

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", response_model=schemas.Token)
def login_user(
    user_creds: deps.PasswordRequestForm,
    db: deps.DBSession
):
    user = db.query(models.User).filter(models.User.email == user_creds.username).first() # legit

    if user is None or not utils.verify_password(user_creds.password, user.password):
        raise exceptions.credentials_exception

    access_token = oauth2.create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=oauth2.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return schemas.Token(access_token=access_token, token_type="bearer")
