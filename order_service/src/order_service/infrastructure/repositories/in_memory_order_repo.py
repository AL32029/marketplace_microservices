from typing import Optional

from order_service.application.ports.order_repo import OrderRepository
from order_service.domain.entities.order import Order


class InMemoryOrderRepo(OrderRepository):
    def __init__(self):
        self._storage: dict[int, Order] = {}
        self._counter = 1

    async def save(self, order: Order) -> None:
        if order.id is None:
            order.id = self._counter
            self._counter += 1

        self._storage[order.id] = order

    async def get_by_id(self, order_id: int) -> Optional[Order]:
        return self._storage.get(order_id)