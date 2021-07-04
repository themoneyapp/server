from datetime import timedelta

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestFormStrict
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.core.security import get_password_hash
from app.crud import crud_user
from app.helpers.emails import send_reset_password_email
from app.helpers.security import generate_password_reset_token, parse_token_subject
from app.routes.api import deps
from app.schemas import schemas_msg, schemas_token


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
        access_token=security.create_token(user.id, access_token_expires),
        token_type="bearer",
    )


@router.post("/password-recovery/{email}", response_model=schemas_msg.Msg)
def recover_password(email: str, db: Session = Depends(deps.get_db)) -> schemas_msg.Msg:
    """
    Password Recovery
    """
    user = crud_user.user.get_by_email(db, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )

    password_reset_token = generate_password_reset_token(email=email)
    send_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    return schemas_msg.Msg(msg="Password recovery email sent")


@router.post("/reset-password/", response_model=schemas_msg.Msg)
def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
    db: Session = Depends(deps.get_db),
) -> schemas_msg.Msg:
    """
    Reset password
    """
    email = parse_token_subject(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")

    user = crud_user.user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )

    elif not crud_user.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")

    hashed_password = get_password_hash(new_password)
    user.hashed_password = hashed_password
    db.add(user)
    db.commit()
    return schemas_msg.Msg(msg="Password updated successfully")
