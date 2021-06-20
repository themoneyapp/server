from typing import Dict

from fastapi.testclient import TestClient

from app.core.config import settings
from app.schemas import schemas_token, schemas_user

from tests import constants


def test_get_access_token(client: TestClient) -> None:
    login_data = {
        "username": constants.TEST_SUPERUSER_EMAIL,
        "password": constants.TEST_SUPERUSER_PASSWORD,
        "grant_type": "password",
    }
    r = client.post(f"{settings.API_V1_PATH}/auth/access-token", data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]
    schemas_token.Token(**tokens)


def test_use_access_token(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = client.get(
        f"{settings.API_V1_PATH}/users/me",
        headers=superuser_token_headers,
    )
    result = r.json()
    assert r.status_code == 200
    assert "email" in result
    assert result["email"] == constants.TEST_SUPERUSER_EMAIL
    assert schemas_user.User(**result)
