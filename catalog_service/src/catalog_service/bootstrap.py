from sqlalchemy.ext.asyncio import AsyncSession

from catalog_service.application.services.create_product import CreateProductUseCase
from catalog_service.application.services.get_all_products import GetAllProductsUseCase
from catalog_service.application.services.get_stock import GetStockUseCase
from catalog_service.application.services.reserve_stock import ReserveStockUseCase
from catalog_service.infrastructure.repositories.sqlalchemy_project_repo import SQLAlchemyProductRepo


def build_services() -> dict:
    async def create_product_use_case(session: AsyncSession):
        repo = SQLAlchemyProductRepo(session)
        return CreateProductUseCase(repo)

    async def get_stock_use_case(session: AsyncSession):
        repo = SQLAlchemyProductRepo(session)
        return GetStockUseCase(repo)

    async def reserve_stock_use_case(session: AsyncSession):
        repo = SQLAlchemyProductRepo(session)
        return ReserveStockUseCase(repo)

    async def get_all_products_use_case(session: AsyncSession):
        repo = SQLAlchemyProductRepo(session)
        return GetAllProductsUseCase(repo)

    return {
        'create_product_use_case': create_product_use_case,
        'get_stock_use_case': get_stock_use_case,
        'reserve_stock_use_case': reserve_stock_use_case,
        'get_all_products_use_case': get_all_products_use_case,
    }
