from typing import Optional

from pydantic import BaseModel, Field
from app.schemas.common import PyObjectId


class UserBase(BaseModel):
    username: str
    is_superuser: bool


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    is_superuser: Optional[bool] = None
    password: Optional[str] = None


class User(UserBase):
    id: PyObjectId = Field(alias="_id")
