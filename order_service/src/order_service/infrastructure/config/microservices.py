from pydantic_settings import SettingsConfigDict, BaseSettings


class CatalogClientSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="CATALOG_",
        env_file=".env",
        extra="ignore"
    )

    service_url: str = "http://localhost:8001"