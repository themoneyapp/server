from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.main import app

from tests import constants
from tests.utils.user import authentication_token_from_email


@pytest.fixture(scope="session")
def db() -> Generator[Session, None, None]:
    yield SessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c  # type: ignore


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session) -> Dict[str, str]:
    return authentication_token_from_email(
        client=client, email=constants.EMAIL_TEST_USER, db=db
    )


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient, db: Session) -> Dict[str, str]:
    return authentication_token_from_email(
        client=client, email=constants.TEST_SUPERUSER_EMAIL, db=db
    )
