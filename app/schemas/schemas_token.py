from typing_extensions import TypedDict

from .base import BaseModel


class TokenPayload(TypedDict):
    exp: int
    sub: str
    nbf: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayloadModel(BaseModel):
    data: TokenPayload
