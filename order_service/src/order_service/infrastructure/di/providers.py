from typing import AsyncIterable

from dishka import Provider, provide, Scope
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine, async_sessionmaker

from order_service.application.ports.order_repo import OrderRepository
from order_service.application.services.create_order import CreateOrderUseCase
from order_service.infrastructure.clients.http_catalog_client import HTTPCatalogClient
from order_service.infrastructure.config import DatabaseSettings
from order_service.infrastructure.repositories.sqlalchemy_order_repo import SQLAlchemyOrderRepo


class DatabaseProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_engine(self, settings: DatabaseSettings) -> AsyncEngine:
        engine = create_async_engine(
            settings.DB_URL.unicode_string(),
            echo=False,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20,
        )
        return engine

    @provide
    def provide_session_maker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            bind=engine,
            expire_on_commit=False,
            class_=AsyncSession,
            autoflush=False,
        )

    @provide
    async def provide_session(self, session_maker: async_sessionmaker[AsyncSession]) -> AsyncSession:
        async with session_maker() as session:
            yield session


class OrderProvider(Provider):
    @provide(scope=Scope.APP)
    def catalog_client(self, request: Request) -> HTTPCatalogClient:
        catalog_url = request.app.state.settings.CATALOG_URL
        return HTTPCatalogClient(base_url=catalog_url)

    @provide(scope=Scope.REQUEST)
    async def db_order_repo(self, session: AsyncSession) -> OrderRepository:
        return SQLAlchemyOrderRepo(session)

    @provide(scope=Scope.REQUEST)
    async def create_order_use_case(self, repo: OrderRepository,
                                    catalog_client: HTTPCatalogClient) -> CreateOrderUseCase:
        return CreateOrderUseCase(repo, catalog_client)
