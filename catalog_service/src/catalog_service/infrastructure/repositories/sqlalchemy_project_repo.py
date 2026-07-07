from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from catalog_service.application.ports.product_repo import ProductRepository
from catalog_service.domain.entities.product import Product
from catalog_service.infrastructure.db.mappers import domain_to_orm, orm_to_domain
from catalog_service.infrastructure.db.models import ProductORM


class SQLAlchemyProductRepo(ProductRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, product: Product) -> None:
        product_orm = domain_to_orm(product)

        merged_orm = await self.session.merge(product_orm)
        await self.session.commit()

        if product.id is None:
            product.id = merged_orm.id

    async def get_by_id(self, product_id: int) -> Optional[Product]:
        product = await self.session.get(ProductORM, product_id)

        if product is None:
            return None

        return orm_to_domain(product)
