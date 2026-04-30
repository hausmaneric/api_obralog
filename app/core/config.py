from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ObraLog API"
    database_url: str = Field(default="sqlite:///./obralog.db", alias="DATABASE_URL")
    secret_key: str = Field(default="obralog-dev-secret-change-me", alias="SECRET_KEY")
    access_token_expire_minutes: int = Field(default=60 * 12, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    auto_create_tables: bool = Field(default=True, alias="AUTO_CREATE_TABLES")
    cors_origins: str = Field(default="*", alias="CORS_ORIGINS")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()


def get_cors_origins() -> list[str]:
    origins = [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]
    return origins or ["*"]
