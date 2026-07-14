import pytest
from dishka import FromDishka, make_async_container
from dishka.integrations.fastapi import FastapiProvider
from httpx import ASGITransport, AsyncClient

from catalog_service.application.ports.product_repo import ProductRepository
from catalog_service.application.services.create_product import CreateProductUseCase
from catalog_service.application.services.get_all_products import GetAllProductsUseCase
from catalog_service.application.services.get_stock import GetStockUseCase
from catalog_service.application.services.reserve_stock import ReserveStockUseCase
from catalog_service.infrastructure.repositories.sqlalchemy_product_repo import (
    SQLAlchemyProductRepo,
)


@pytest.fixture(scope="function")
async def test_container(async_session):
    from dishka import Provider, Scope, provide

    class TestCatalogProvider(Provider):
        @provide(scope=Scope.REQUEST)
        async def db_product_repo(self) -> ProductRepository:
            return SQLAlchemyProductRepo(async_session)

        @provide(scope=Scope.REQUEST)
        async def create_product_use_case(self, db_repo: FromDishka[ProductRepository]) -> CreateProductUseCase:
            return CreateProductUseCase(db_repo)

        @provide(scope=Scope.REQUEST)
        async def all_products_use_case(self, db_repo: FromDishka[ProductRepository]) -> GetAllProductsUseCase:
            return GetAllProductsUseCase(db_repo)

        @provide(scope=Scope.REQUEST)
        async def get_stock_use_case(self, db_repo: FromDishka[ProductRepository]) -> GetStockUseCase:
            return GetStockUseCase(db_repo)

        @provide(scope=Scope.REQUEST)
        async def reserve_stock_use_case(self, db_repo: FromDishka[ProductRepository]) -> ReserveStockUseCase:
            return ReserveStockUseCase(db_repo)

    container = make_async_container(
        TestCatalogProvider(),
        FastapiProvider(),
    )
    yield container
    await container.close()


@pytest.fixture(scope="function")
def test_app(test_container):
    from catalog_service.main import create_app
    return create_app(enable_lifespan=False, container=test_container)


@pytest.fixture(scope="function")
async def client(test_app):
    async with AsyncClient(
        transport=ASGITransport(app=test_app),
        base_url="http://test"
    ) as client:
        yield client
