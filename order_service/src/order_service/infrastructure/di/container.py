from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider

from .providers import OrderProvider, DatabaseProvider
from ..config import DatabaseSettings


def get_dishka_container():
    database_settings = DatabaseSettings()

    return make_async_container(
        DatabaseProvider(),
        OrderProvider(),
        FastapiProvider(),
        context={DatabaseSettings: database_settings}
    )