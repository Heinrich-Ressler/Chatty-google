from fastapi import FastAPI
from app.api.routes import auth, google
from app.db.session import engine
from app.db.base import Base
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(google.router, prefix="/auth/google", tags=["Google OAuth2"])

