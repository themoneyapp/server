from datetime import datetime, timedelta
from typing import Any, Optional, Union

from jose import jwt
from passlib.context import CryptContext
from pydantic import ValidationError

from app.core.config import settings
from app.schemas.schemas_token import TokenPayload, TokenPayloadModel


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def create_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    now = datetime.utcnow()
    if expires_delta is not None:
        expire = now + expires_delta

    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    expire_ts = int(expire.timestamp())
    now_ts = int(now.timestamp())
    to_encode = TokenPayload(exp=expire_ts, nbf=now_ts, sub=str(subject))
    encoded_jwt: str = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def parse_token(token: str) -> Optional[TokenPayload]:
    try:
        token_data: TokenPayload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[ALGORITHM]
        )
        return TokenPayloadModel(data=token_data).data

    except (jwt.JWTError, ValidationError):
        return None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)  # type: ignore


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)  # type: ignore
