import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class JWTSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.getenv('JWT_ENV_PATH', '/vault/secrets/jwt_token.env'),
        extra='forbid'
    )

    SECRET_KEY: str
    ALGORITHM: str = 'HS256'
