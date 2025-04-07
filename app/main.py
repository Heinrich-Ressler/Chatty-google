from fastapi import FastAPI
from app.api.routes import auth
from app.core.config import settings
from app.api.v1.routes import password

app.include_router(password.router, prefix="/api/v1", tags=["password"])
app = FastAPI(title="Auth Service")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
