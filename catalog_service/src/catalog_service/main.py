from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from catalog_service.bootstrap import build_services
from catalog_service.infrastructure.config import DatabaseSettings
from catalog_service.presentation.api.product_router import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    database_settings = DatabaseSettings()
    engine = create_async_engine(database_settings.DB_URL.unicode_string())
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    app.state.db_engine = engine
    app.state.db_session = session_maker

    services = build_services()

    app.state.services = services

    yield

    await app.state.db_engine.dispose()


app = FastAPI(title="Catalog Service", lifespan=lifespan)
app.include_router(router)
