import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from order_service.bootstrap import build_services
from order_service.infrastructure.config import DatabaseSettings
from order_service.presentation.api.order_router import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    database_settings = DatabaseSettings()
    engine = create_async_engine(database_settings.DB_URL.unicode_string())
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    app.state.db_engine = engine
    app.state.db_session = session_maker

    services = build_services(os.getenv('CATALOG_SERVICE_URL'))

    app.state.services = services

    yield

    await app.state.db_engine.dispose()


app = FastAPI(title="Order Service", lifespan=lifespan)
app.include_router(router)
