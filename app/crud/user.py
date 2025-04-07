from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User

async def get_user_by_email(session: AsyncSession, email: str):
    result = await session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def create_user(session: AsyncSession, email: str, name: str = None):
    new_user = User(email=email, name=name)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user
