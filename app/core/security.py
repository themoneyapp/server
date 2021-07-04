from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from passlib.context import CryptContext
from pydantic import ValidationError

from app.core.config import settings
from app.schemas.schemas_token import TokenPayload, TokenPayloadModel


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def create_token(subject: str, expires_delta: timedelta) -> str:
    """Create a JWT token for the given `subject`.

    Args:
        subject (str): Subject of the token.
        expires_delta (timedelta): Token expiry timedelta

    Returns:
        str: A JWT string
    """
    now = datetime.utcnow()
    expire = now + expires_delta

    expire_ts = int(expire.timestamp())
    now_ts = int(now.timestamp())
    to_encode = TokenPayload(exp=expire_ts, nbf=now_ts, sub=str(subject))
    encoded_jwt: str = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def parse_token(token: str) -> Optional[TokenPayload]:
    """Parse a JWT token.

    Args:
        token (str): JWT token as string.

    Returns:
        Optional[TokenPayload]: parsed Token payload
    """
    try:
        token_data: TokenPayload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[ALGORITHM]
        )
        return TokenPayloadModel(data=token_data).data

    except (jwt.JWTError, ValidationError):
        return None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain text password against hashed password in db.

    Args:
        plain_password (str): Plain text password to check.
        hashed_password (str): Hashed password to checked with.

    Returns:
        bool: Whether hash of plain text matches with the hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)  # type: ignore


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)  # type: ignore
