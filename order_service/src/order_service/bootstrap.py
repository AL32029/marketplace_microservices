import os

from sqlalchemy.ext.asyncio import async_sessionmaker

from order_service.application.services.create_order import CreateOrderUseCase
from order_service.infrastructure.clients.http_catalog_client import HTTPCatalogClient
from order_service.infrastructure.repositories.sqlalchemy_order_repo import SQLALchemyOrderRepo


def build_services(session_maker: async_sessionmaker) -> dict:
    catalog_client = HTTPCatalogClient(base_url=os.getenv("CATALOG_SERVICE_URL", "http://catalog-service"))

    async def get_use_case():
        async with session_maker() as session:
            repo = SQLALchemyOrderRepo(session)
            return CreateOrderUseCase(repo, catalog_client)

    return {
        "create_order_use_case": get_use_case
    }