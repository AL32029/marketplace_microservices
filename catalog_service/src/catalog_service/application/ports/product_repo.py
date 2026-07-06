from abc import ABC, abstractmethod
from typing import Optional

from catalog_service.src.catalog_service.domain.entities.product import Product


class ProductRepository(ABC):
    @abstractmethod
    async def get_by_id(self, product_id: int) -> Optional[Product]:
        raise NotImplemented

    @abstractmethod
    async def save(self, product: Product) -> None:
        pass
