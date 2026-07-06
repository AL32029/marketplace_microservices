from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from order_service.application.ports.order_repo import OrderRepository
from order_service.domain.entities.order import Order
from order_service.infrastructure.db.mappers import domain_to_orm, orm_to_domain
from order_service.infrastructure.db.models import OrderORM


class SQLALchemyOrderRepo(OrderRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, order: Order) -> None:
        orm_order = domain_to_orm(order)
        self.session.add(orm_order)
        await self.session.commit()
        order.id = orm_order.id

    async def get_by_id(self, order_id: int) -> Optional[Order]:
        order = await self.session.get(OrderORM, order_id)

        if order is None:
            return None

        return orm_to_domain(order)