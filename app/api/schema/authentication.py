from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    is_admin: Optional[bool] = False

class UserResponse(UserBase):
    id: int
    is_admin: Optional[bool] = False

class Token(BaseModel):
    access_token: str
    token_type: str