from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider

from .providers import CatalogProvider


def get_dishka_container():
    return make_async_container(
        CatalogProvider(),
        FastapiProvider()
    )
