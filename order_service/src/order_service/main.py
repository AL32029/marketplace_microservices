import os
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from order_service.infrastructure.config import DatabaseSettings
from order_service.infrastructure.di import get_dishka_container
from order_service.presentation.api.order_router import router


def create_app(container=None) -> FastAPI:
    app = FastAPI(title="Order Service")
    app.state.catalog_url = os.getenv('CATALOG_SERVICE_URL')

    if container is None:
        container = get_dishka_container()

    setup_dishka(container, app)

    app.include_router(router)

    return app


app = create_app()
