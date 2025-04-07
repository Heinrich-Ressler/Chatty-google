from fastapi import APIRouter, Depends, Request
from starlette.responses import RedirectResponse
from app.core.security import oauth, get_user_info
from app.db.session import get_async_session
from app.crud.user import get_user_by_email, create_user
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.get("/google")
async def login_via_google():
    redirect_uri = "http://localhost:8000/api/v1/auth/google/callback"
    return await oauth.google.authorize_redirect(Request(scope={}, receive=None), redirect_uri)

@router.get("/google/callback")
async def google_callback(request: Request, session: AsyncSession = Depends(get_async_session)):
    token = await oauth.google.authorize_access_token(request)
    user_info = await get_user_info(token)
    email = user_info.get("email")
    name = user_info.get("name")
    
    user = await get_user_by_email(session, email)
    if not user:
        user = await create_user(session, email=email, name=name)
    
    return {"message": "User authenticated", "user": {"email": user.email, "name": user.name}}
