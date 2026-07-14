import asyncio
import os
import subprocess
import sys
from typing import AsyncIterable
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider
from fastapi import Request
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from testcontainers.postgres import PostgresContainer

from order_service.application.ports.order_repo import OrderRepository
from order_service.application.services.create_order import CreateOrderUseCase
from order_service.infrastructure.clients.http_catalog_client import HTTPCatalogClient
from order_service.infrastructure.repositories.sqlalchemy_order_repo import SQLAlchemyOrderRepo

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer('postgres:17') as postgres:
        db_url = postgres.get_connection_url(driver='asyncpg')
        os.environ["DATABASE_URL"] = db_url
        subprocess.run(
            ["alembic", "-c", "alembic.ini", "upgrade", "head"],
            check=True,
            env=os.environ,
        )
        yield postgres


@pytest_asyncio.fixture(scope="function")
async def async_engine(postgres_container):
    engine = create_async_engine(
        os.environ["DATABASE_URL"],
        echo=False,
        pool_size=5,
        pool_pre_ping=True,
    )
    yield engine
    await engine.dispose()


async def _truncate_all_tables(async_engine):
    async with async_engine.connect() as conn:
        await conn.execute(text("SET session_replication_role = 'replica';"))
        result = await conn.execute(text(
            "SELECT tablename FROM pg_tables WHERE schemaname = 'public' "
            "AND tablename != 'alembic_version';"
        ))
        tables = [row[0] for row in result]
        for table in tables:
            await conn.execute(text(f'TRUNCATE TABLE "{table}" RESTART IDENTITY CASCADE;'))
        await conn.execute(text("SET session_replication_role = 'origin';"))
        await conn.commit()


@pytest_asyncio.fixture(scope="function")
async def async_session(async_engine):
    await _truncate_all_tables(async_engine)

    async_session_maker = async_sessionmaker(
        async_engine,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope="function")
async def test_container(async_session):
    from dishka import Provider, Scope, provide

    class TestOrderProvider(Provider):
        @provide(scope=Scope.REQUEST)
        def catalog_client(self) -> HTTPCatalogClient:
            return AsyncMock()

        @provide(scope=Scope.REQUEST)
        async def get_db(self, request: Request) -> AsyncIterable[AsyncSession]:
            async with request.app.state.db_session() as session:
                yield session

        @provide(scope=Scope.REQUEST)
        async def db_order_repo(self, session: AsyncSession) -> OrderRepository:
            return SQLAlchemyOrderRepo(session)

        @provide(scope=Scope.REQUEST)
        async def create_order_use_case(self, repo: OrderRepository,
                                        catalog_client: HTTPCatalogClient) -> CreateOrderUseCase:
            return CreateOrderUseCase(repo, catalog_client)

    container = make_async_container(
        TestOrderProvider(),
        FastapiProvider(),
    )
    yield container
    await container.close()


@pytest.fixture(scope="function")
def test_app(test_container):
    from catalog_service.main import create_app
    return create_app(container=test_container)


@pytest.fixture(scope="function")
async def client(test_app):
    async with AsyncClient(
            transport=ASGITransport(app=test_app),
            base_url="http://test"
    ) as client:
        yield client
