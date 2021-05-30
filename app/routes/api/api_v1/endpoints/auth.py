from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestFormStrict
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.crud import crud_user
from app.routes.api import deps
from app.schemas import schemas_token


router = APIRouter()


@router.post("/auth/access-token", response_model=schemas_token.Token)
def get_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestFormStrict = Depends(),
) -> schemas_token.Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud_user.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    elif not crud_user.user.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return schemas_token.Token(
        access_token=security.create_token(user.id, expires_delta=access_token_expires),
        token_type="bearer",
    )
