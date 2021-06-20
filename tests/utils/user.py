from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import get_password_hash
from app.crud import crud_user
from app.models import models_user
from app.schemas.schemas_user import UserCreate, UserUpdate

from tests import constants
from tests.utils.utils import random_email, random_lower_string


def user_authentication_headers(
    *, client: TestClient, email: str, password: str
) -> Dict[str, str]:
    data = {"username": email, "password": password, "grant_type": "password"}

    r = client.post(f"{settings.API_V1_PATH}/auth/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def create_random_user(
    db: Session, email: str = random_email(), password: str = random_lower_string()
) -> models_user.User:
    user = crud_user.user.get_by_email(db, email=email)
    if user is None:
        user_in = UserCreate(
            email=email,
            password=password,
            full_name="Test User",
        )
        user = crud_user.user.create(db=db, obj_in=user_in)
    else:
        user_updata_in = UserUpdate(password=password)
        user = crud_user.user.update(db, db_obj=user, obj_in=user_updata_in)

        # user.hashed_password = get_password_hash(password)
    return user


def create_superuser(db: Session) -> models_user.User:
    user = crud_user.user.get_by_email(db, email=constants.TEST_SUPERUSER_EMAIL)
    if user is None:
        user_in = UserCreate(
            email=constants.TEST_SUPERUSER_EMAIL,
            password=constants.TEST_SUPERUSER_PASSWORD,
            full_name="Test Superuser",
            is_admin=True,
            is_superuser=True,
        )
        user = crud_user.user.create(db, obj_in=user_in)  # noqa: F841

    return user


def authentication_token_from_email(
    *, client: TestClient, email: str, db: Session
) -> Dict[str, str]:
    """
    Return a valid token for the user with given email.

    If the user doesn't exist it is created first.
    """
    password = random_lower_string()

    if email == constants.TEST_SUPERUSER_EMAIL:
        create_superuser(db)
        password = constants.TEST_SUPERUSER_PASSWORD
    else:
        create_random_user(db, email=email, password=password)

    return user_authentication_headers(client=client, email=email, password=password)
