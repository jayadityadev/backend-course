from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    database_url: Optional[str] = None

    db_username: Optional[str] = None
    db_password: Optional[str] = None
    db_hostname: Optional[str] = None
    db_port: Optional[str] = None
    db_name: Optional[str] = None

    jwt_secret_key: str
    jwt_algorithm: str
    jwt_expire_time: int

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()


if settings.database_url:
    db_url = settings.database_url.replace(
        "postgresql://", "postgresql+psycopg://", 1
    )
else:
    db_url = (
        f"postgresql+psycopg://"
        f"{settings.db_username}:{settings.db_password}"
        f"@{settings.db_hostname}:{settings.db_port}/{settings.db_name}"
    )
