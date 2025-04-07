# app/repositories/user.py
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
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


async def create_user(user: User, session: AsyncSession = None) -> User:
    if session is None:
        async with get_async_session() as session:
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user
    else:
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


async def update_user_password(user_id: int, hashed_password: str) -> None:
    async with get_async_session() as session:
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(password=hashed_password)
        )
        await session.execute(stmt)
        await session.commit()

