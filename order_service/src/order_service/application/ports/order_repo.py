from abc import ABC, abstractmethod
from typing import Optional

from order_service.domain.entities.order import Order


class OrderRepository(ABC):
    @abstractmethod
    async def save(self, order: Order) -> None:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, order_id: int) -> Optional[Order]:
        raise NotImplemented
