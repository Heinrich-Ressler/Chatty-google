from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.db.session import get_db
from app.schemas.user import UserCreate
from app.services import auth as auth_service
from app.utils.security import create_access_token

import pathlib

router = APIRouter()
SCOPES = ["openid", "https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email"]
CLIENT_SECRETS_FILE = pathlib.Path(settings.CLIENT_SECRET_FILE)

@router.get("/auth/callback")
async def callback(request: Request, db: AsyncSession = Depends(get_db)):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="No code provided by Google")

    flow = Flow.from_client_secrets_file(
        str(CLIENT_SECRETS_FILE),
        scopes=SCOPES,
        redirect_uri=settings.GOOGLE_REDIRECT_URI
    )
    flow.fetch_token(code=code)
    credentials = flow.credentials
    token = credentials.id_token

    try:
        id_info = id_token.verify_oauth2_token(token, requests.Request(), settings.GOOGLE_CLIENT_ID)
    except Exception:
        raise HTTPException(status_code=403, detail="Invalid token")

    email = id_info.get("email")
    name = id_info.get("name")
    picture = id_info.get("picture")

    user = await auth_service.get_user_by_email(email=email, db=db)
    if not user:
        nickname = email.split("@")[0]
        user_create = UserCreate(email=email, name=name, nickname=nickname, picture=picture)
        user = await auth_service.create_user(user_create, db)

    access_token = create_access_token(data={"sub": str(user.id)})

    return JSONResponse({
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "nickname": user.nickname,
            "name": user.name,
            "picture": user.picture
        }
    })