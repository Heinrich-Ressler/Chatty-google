from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    picture: Optional[str] = None

class UserCreate(UserBase):
    nickname: str

class UserOut(UserBase):
    id: int
    nickname: Optional[str]
    is_active: bool

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    nickname: str