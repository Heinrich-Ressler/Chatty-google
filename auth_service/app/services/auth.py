from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

async def get_user_by_email(email: str, db: AsyncSession) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()

async def create_user(user_in: UserCreate, db: AsyncSession) -> User:
    new_user = User(**user_in.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def update_user_nickname(user_id: int, nickname: str, db: AsyncSession) -> User:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    user.nickname = nickname
    await db.commit()
    await db.refresh(user)
    return user

async def delete_user(user_id: int, db: AsyncSession):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if user:
        await db.delete(user)
        await db.commit()