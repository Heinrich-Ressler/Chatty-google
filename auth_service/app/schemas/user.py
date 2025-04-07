from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    is_active: bool

    class Config:
        orm_mode = True


class UserRead(BaseModel):
    id: str
    email: EmailStr
    full_name: Optional[str]
    is_active: bool
    is_verified: bool


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
