from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from catalog_service.infrastructure.config import DatabaseSettings
from catalog_service.infrastructure.di import get_dishka_container
from catalog_service.presentation.api.product_router import router


def create_app(enable_lifespan: bool = True, container=None) -> FastAPI:
    app = FastAPI(title="Catalog Service")

    if container is None:
        container = get_dishka_container()

    setup_dishka(container, app)

    app.include_router(router)

    return app


app = create_app()
