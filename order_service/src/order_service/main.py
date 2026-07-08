import os

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from order_service.bootstrap import build_services
from order_service.presentation.api.order_router import router


def create_app():
    db_url = os.getenv("DB_URL", "postgresql+asyncpg://user:pass@localhost/orders_db")
    engine = create_async_engine(db_url)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    catalog_url: str = os.getenv('CATALOG_SERVICE_URL')

    services = build_services(session_maker, catalog_url)

    app = FastAPI(title="Order Service")

    app.state.session_maker = session_maker
    app.state.services = services

    app.include_router(router)

    return app


app = create_app()
