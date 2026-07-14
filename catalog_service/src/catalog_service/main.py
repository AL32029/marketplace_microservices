from fastapi import FastAPI
from dishka.integrations.fastapi import setup_dishka

from catalog_service.infrastructure.di import get_dishka_container
from catalog_service.presentation.api.product_router import router


def create_app(container=None) -> FastAPI:
    app = FastAPI(title="Catalog Service")

    if container is None:
        container = get_dishka_container()

    setup_dishka(container, app)
    app.include_router(router)

    return app


app = create_app()