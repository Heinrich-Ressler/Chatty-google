from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from app.repositories.user import get_user_by_email, create_user
from app.services.email import send_email

async def register_user(session: AsyncSession, user_in: UserCreate):
    existing_user = await get_user_by_email(session, user_in.email)
    if existing_user:
        return None

    user = await create_user(session, user_in)
    confirmation_link = f"http://localhost:8000/confirm?email={user.email}"
    send_email(user.email, "Confirm your account", f"Click to confirm: {confirmation_link}")
    return user
