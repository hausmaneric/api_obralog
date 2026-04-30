from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ObraLog API"
    database_url: str = Field(default="sqlite:///./obralog.db", alias="DATABASE_URL")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
