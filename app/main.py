from fastapi import FastAPI
from app.api.v1.routes.google_auth import router as google_auth_router

app = FastAPI(title="Auth Service")

app.include_router(google_auth_router, prefix="/api/v1/auth", tags=["Google Auth"])
