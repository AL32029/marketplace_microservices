from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from catalog_service.application.ports.product_repo import ProductRepository
from catalog_service.application.services.create_product import CreateProductUseCase
from catalog_service.application.services.get_all_products import GetAllProductsUseCase
from catalog_service.application.services.get_stock import GetStockUseCase
from catalog_service.application.services.reserve_stock import ReserveStockUseCase
from catalog_service.infrastructure.repositories.sqlalchemy_product_repo import (
    SQLAlchemyProductRepo,
)


class CatalogProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_db(self, request: Request) -> AsyncIterable[AsyncSession]:
        async with request.app.state.db_session() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    async def db_product_repo(self, session: AsyncSession) -> ProductRepository:
        return SQLAlchemyProductRepo(session)

    @provide(scope=Scope.REQUEST)
    async def create_product_use_case(self, db_repo: ProductRepository) -> CreateProductUseCase:
        return CreateProductUseCase(db_repo)

    @provide(scope=Scope.REQUEST)
    async def all_products_use_case(self, db_repo: ProductRepository) -> GetAllProductsUseCase:
        return GetAllProductsUseCase(db_repo)

    @provide(scope=Scope.REQUEST)
    async def get_stock_use_case(self, db_repo: ProductRepository) -> GetStockUseCase:
        return GetStockUseCase(db_repo)

    @provide(scope=Scope.REQUEST)
    async def reserve_stock_use_case(self, db_repo: ProductRepository) -> ReserveStockUseCase:
        return ReserveStockUseCase(db_repo)
