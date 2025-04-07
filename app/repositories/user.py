from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from app.models.user import User
from app.db.session import get_async_session

async def get_user_by_email(email: str, session: AsyncSession = None) -> User | None:
    if session is None:
        async with get_async_session() as session:
            result = await session.execute(select(User).where(User.email == email))
    else:
        result = await session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def get_user_by_id(user_id: int, session: AsyncSession = None) -> User | None:
    if session is None:
        async with get_async_session() as session:
            result = await session.execute(select(User).where(User.id == user_id))
    else:
        result = await session.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def update_user_password(user_id: int, hashed_password: str) -> None:
    async with get_async_session() as session:
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(password=hashed_password)
        )
        await session.execute(stmt)
        await session.commit()
