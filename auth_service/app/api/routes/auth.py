from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.services.auth import register_user, authenticate_user, confirm_email_token, send_confirmation_email
from app.api.deps import get_current_user
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register(user_data: UserCreate, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    user = await register_user(user_data, db)
    await send_confirmation_email(user.email, background_tasks)
    return user

@router.get("/confirm")
async def confirm_email(token: str, db: AsyncSession = Depends(get_db)):
    user = await confirm_email_token(token, db)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    return {"message": "Email confirmed successfully"}

@router.post("/login")
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    token = await authenticate_user(user_data, db)
    if not token:
        raise HTTPException(status_code=400, detail="Invalid credentials or unconfirmed email")
    return {"access_token": token, "token_type": "bearer"}
