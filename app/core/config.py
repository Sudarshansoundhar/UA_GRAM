from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "SUPER_SECRET_KEY_FOR_DEVELOPMENT_123456"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

settings = Settings()
