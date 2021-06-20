from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import parse_token
from app.crud import crud_user
from app.db.session import SessionLocal
from app.models import models_user


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PATH}/auth/access-token"
)


def get_db() -> Generator[Session, None, None]:
    try:
        db = SessionLocal()
        yield db

    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models_user.User:
    token_data = parse_token(token)
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    user = crud_user.user.get(db, id=token_data["sub"])
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


def get_current_active_user(
    current_user: models_user.User = Depends(get_current_user),
) -> models_user.User:
    if not crud_user.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user


def get_current_active_superuser(
    current_user: models_user.User = Depends(get_current_user),
) -> models_user.User:
    if not crud_user.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )

    return current_user
