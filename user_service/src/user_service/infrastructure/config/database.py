import os

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.getenv('DATABASE_ENV_PATH', '/vault/secrets/database.env'),
        extra='forbid'
    )

    DB_HOST: str
    DB_PORT: int

    DB_USER: str
    DB_PASSWORD: str

    DB_DATABASE: str

    @property
    def DB_URL(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme='postgresql+asyncpg',
            host=self.DB_HOST,
            port=self.DB_PORT,
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            path=f'/{self.DB_DATABASE}'
        )
