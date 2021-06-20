from typing import Optional

from pydantic import EmailStr

from .base import BaseModel


# Shared properties
class UserBase(BaseModel):
    full_name: str
    email: Optional[EmailStr] = None
    is_active: bool = True
    is_admin: bool = False
    is_superuser: bool = False


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: str

    class Config(BaseModel.Config):
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
