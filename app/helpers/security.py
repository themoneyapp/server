from datetime import timedelta
from typing import Optional

from app.core.config import settings
from app.core.security import create_token, parse_token


def generate_password_reset_token(email: str) -> str:
    expires_delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    return create_token(email, expires_delta=expires_delta)


def parse_token_subject(token: str) -> Optional[str]:
    data = parse_token(token)
    if data is None:
        return None
    return data["sub"]
