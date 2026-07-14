from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider

from catalog_service.infrastructure.config import DatabaseSettings
from .providers import CatalogProvider, DatabaseProvider


def get_dishka_container():
    database_settings = DatabaseSettings()

    return make_async_container(
        DatabaseProvider(),
        CatalogProvider(),
        FastapiProvider(),
        context={DatabaseSettings: database_settings}
    )
