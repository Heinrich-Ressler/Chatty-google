from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status, BackgroundTasks
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.core.security import get_password_hash, verify_password, create_access_token
from app.services.email import generate_confirmation_token, verify_confirmation_token, send_email_async

async def register_user(user_data: UserCreate, db: AsyncSession):
    result = await db.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        is_active=False,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def authenticate_user(user_data: UserLogin, db: AsyncSession):
    result = await db.execute(select(User).where(User.email == user_data.email))
    user = result.scalar_one_or_none()
    if not user or not user.is_active:
        return None
    if not verify_password(user_data.password, user.hashed_password):
        return None
    return create_access_token({"sub": str(user.id)})

async def confirm_email_token(token: str, db: AsyncSession):
    email = verify_confirmation_token(token)
    if not email:
        return None
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user:
        return None
    user.is_active = True
    await db.commit()
    return user

async def send_confirmation_email(email: str, background_tasks: BackgroundTasks):
    token = generate_confirmation_token(email)
    confirm_url = f"http://localhost:8000/auth/confirm?token={token}"
    subject = "Confirm your email"
    body = f"Click to confirm your registration: {confirm_url}"
    background_tasks.add_task(send_email_async, email, subject, body)
