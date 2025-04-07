from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PROJECT_NAME: str = "Auth Service"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    EMAILS_FROM_EMAIL: str
    EMAILS_FROM_NAME: str = "Chatty Support"

    BACKEND_CORS_ORIGINS: list[str] = ["*"]
    SQLALCHEMY_DATABASE_URI: str

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

settings = Settings()
