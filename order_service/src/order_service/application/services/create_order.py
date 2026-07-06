from typing import List

from order_service.application.ports.catalog_repo import CatalogClient
from order_service.application.ports.order_repo import OrderRepository
from order_service.domain.entities.order import Order, OrderItem
from order_service.domain.exceptions.catalog_errors import CatalogUnavailableError, ProductNotFoundError


class CreateOrderUseCase:
    def __init__(self, order_repo: OrderRepository, catalog_client: CatalogClient):
        self.order_repo = order_repo
        self.catalog_client = catalog_client

    async def execute(self, user_id: int, items: List[OrderItem]) -> Order:
        order = Order(user_id=user_id)

        # TODO: Реализовать batch-обработку
        for item in items:
            try:
                in_stock = await self.catalog_client.check_stock(item.product_id, item.quantity)
                if not in_stock:
                    raise ValueError(f"Product {item.product_id} has insufficient stock")
            except (CatalogUnavailableError, ProductNotFoundError) as e:
                raise ValueError(f"Cannot verify stock for product {item.product_id}: {e}") from e

            order.add_item(
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.price
            )

        await self.order_repo.save(order)
        return order