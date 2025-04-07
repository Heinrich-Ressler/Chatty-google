from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    EMAILS_FROM_EMAIL: str
    EMAILS_FROM_NAME: str
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_HOST: str
    SMTP_PORT: int

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str


settings = Settings()
