from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from user_service.bootstrap import build_services
from user_service.infrastructure.config import DatabaseSettings, JWTSettings
from user_service.presentation.api.user_router import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    database_settings = DatabaseSettings()
    jwt_settings = JWTSettings()
    engine = create_async_engine(database_settings.DB_URL.unicode_string())
    session_maker = async_sessionmaker(engine, expire_on_commit=False)


    app.state.db_engine = engine
    app.state.db_session = session_maker

    services = build_services(jwt_settings)

    app.state.services = services

    yield

    await app.state.db_engine.dispose()


app = FastAPI(title="User Service", lifespan=lifespan)
app.include_router(router)
