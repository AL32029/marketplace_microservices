import os

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from catalog_service.bootstrap import build_services
from catalog_service.presentation.api.product_router import router


def create_app():
    db_url = os.getenv("DB_URL", "postgresql+asyncpg://user:pass@localhost/catalog_service")
    engine = create_async_engine(db_url)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    services = build_services()

    app = FastAPI(title="Order Service")

    app.state.session_maker = session_maker
    app.state.services = services

    app.include_router(router)

    return app


app = create_app()
