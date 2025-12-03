from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from enum import Enum


class UserRole(str, Enum):
    user = "user"
    admin = "admin"


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    role: UserRole

    model_config = ConfigDict(from_attributes=True)
