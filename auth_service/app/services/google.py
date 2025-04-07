from fastapi import Request
from google.oauth2 import id_token
from google.auth.transport import requests as grequests
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.core.security import create_access_token

GOOGLE_CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com"

async def get_google_user(request: Request):
    token = request.query_params.get("token")
    if not token:
        raise ValueError("Missing token")

    try:
        idinfo = id_token.verify_oauth2_token(token, grequests.Request(), GOOGLE_CLIENT_ID)
        return {
            "email": idinfo["email"],
            "full_name": idinfo.get("name", "")
        }
    except ValueError:
        raise ValueError("Invalid token")

async def get_or_create_google_user(token_data: dict, db: AsyncSession):
    result = await db.execute(select(User).where(User.email == token_data["email"]))
    user = result.scalar_one_or_none()

    if not user:
        user = User(
            email=token_data["email"],
            full_name=token_data["full_name"],
            is_active=True,
            is_oauth=True,
            hashed_password=None
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    return {"access_token": create_access_token({"sub": str(user.id)})}
