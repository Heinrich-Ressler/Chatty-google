from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user import UserCreate, UserOut
from app.services.auth import register_user

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register(user_in: UserCreate, session: AsyncSession = Depends(get_db)):
    user = await register_user(session, user_in)
    if not user:
        raise HTTPException(status_code=400, detail="User already exists")
    return user
