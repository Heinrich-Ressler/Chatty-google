from fastapi import APIRouter, Depends, Request
from app.services.google import get_google_user, get_or_create_google_user
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.get("/login")
async def google_oauth_callback(request: Request, db: AsyncSession = Depends(get_db)):
    token_data = await get_google_user(request)
    user = await get_or_create_google_user(token_data, db)
    return {"access_token": user["access_token"], "token_type": "bearer"}
