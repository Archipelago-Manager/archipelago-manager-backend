from typing import Literal
from pydantic import (
        BaseModel,
        AnyUrl,
        PostgresDsn,
        computed_field
        )
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseModel):
    SERVER: str
    PORT: int = 5433
    USER: str
    PASSWORD: str = ""
    DB: str = ""


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
            env_file=".env",
            env_ignore_empty=True,
            env_nested_delimiter='_'
            )

    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    SMOKESHOW_AUTH_KEY: str | None = None

    STORAGE_TYPE: Literal["local", "aws"] = "local"
    LOCAL_STORAGE_ROOT_FOLDER: str | None = None
    AWS_ACCESS_KEY_ID: str | None = None
    AWS_SECRET_ACCESS_KEY: str | None = None
    AWS_BUCKET_NAME: str | None = None
    AWS_ENDPOINT_URL: str | None = None

    DB_BACKEND: Literal["sqlite", "postgres"] = "sqlite"

    SQLITE_FILE_NAME: str | None = f"database_{ENVIRONMENT}.db"

    POSTGRES: PostgresSettings | None = None

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> AnyUrl | PostgresDsn:
        if self.DB_BACKEND == "postgres":
            return MultiHostUrl.build(
                scheme="postgresql+psycopg",
                username=self.POSTGRES.USER,
                password=self.POSTGRES.PASSWORD,
                host=self.POSTGRES.SERVER,
                port=self.POSTGRES.PORT,
                path=self.POSTGRES.DB,
            )
        else:  # Default to sqlite
            return AnyUrl(f"sqlite:///{self.SQLITE_FILE_NAME}")


settings = Settings()
