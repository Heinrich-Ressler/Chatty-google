from fastapi import FastAPI
from app.api.routes import auth
from app.core.config import settings

app = FastAPI(title="Auth Service")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
