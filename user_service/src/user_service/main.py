import os

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from user_service.bootstrap import build_services
from user_service.presentation.api.user_router import router


def create_app():
    db_url = os.getenv("DB_URL", "postgresql+asyncpg://user:pass@localhost/catalog_service")
    engine = create_async_engine(db_url)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    services = build_services()

    app = FastAPI(title="User Service")

    app.state.session_maker = session_maker
    app.state.jwt_secret_key = os.getenv('JWT_SECRET_KEY')
    app.state.jwt_algorithm = os.getenv('JWT_ALGORITHM')
    app.state.services = services

    app.include_router(router)

    return app


app = create_app()
