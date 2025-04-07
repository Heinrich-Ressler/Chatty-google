# app/services/user.py
from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, status
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.models.user import User
from app.repositories.user import get_user_by_email, create_user, update_user_password, get_user_by_id
from app.core.config import settings
from app.utils.email import send_email

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def request_password_reset(email: str) -> None:
    user = await get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = _generate_reset_token(user.id)
    reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}"

    await send_email(
        to=email,
        subject="Password Reset Request",
        body=f"Click the link to reset your password: {reset_link}"
    )


async def confirm_password_reset(token: str, new_password: str) -> None:
    user_id = _verify_reset_token(token)
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    hashed_password = get_password_hash(new_password)
    await update_user_password(user.id, hashed_password)


def _generate_reset_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(hours=1)
    payload = {
        "sub": str(user_id),
        "exp": expire,
        "type": "password_reset"
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def _verify_reset_token(token: str) -> int:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        if payload.get("type") != "password_reset":
            raise HTTPException(status_code=400, detail="Invalid token type")
        return int(payload["sub"])
    except (JWTError, ValueError):
        raise HTTPException(status_code=400, detail="Invalid or expired token")
