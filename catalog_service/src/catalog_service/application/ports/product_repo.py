from abc import ABC, abstractmethod
from typing import Optional, List

from catalog_service.domain.entities.product import Product


class ProductRepository(ABC):
    @abstractmethod
    async def get_all(self) -> List[Product]:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, product_id: int) -> Optional[Product]:
        raise NotImplemented

    @abstractmethod
    async def save(self, product: Product) -> None:
        raise NotImplemented
