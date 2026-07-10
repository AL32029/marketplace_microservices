from sqlalchemy.ext.asyncio import AsyncSession

from order_service.application.services.create_order import CreateOrderUseCase
from order_service.infrastructure.clients.http_catalog_client import HTTPCatalogClient
from order_service.infrastructure.repositories.sqlalchemy_order_repo import SQLAlchemyOrderRepo


def build_services(catalog_url: str) -> dict:
    catalog_client = HTTPCatalogClient(base_url=catalog_url)

    async def create_order_use_case(session: AsyncSession):
        repo = SQLAlchemyOrderRepo(session)
        return CreateOrderUseCase(repo, catalog_client)

    return {
        "create_order_use_case": create_order_use_case
    }
