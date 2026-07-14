from abc import ABC, abstractmethod

from catalog_service.domain.entities.product import Product


class ProductRepository(ABC):
    @abstractmethod
    async def get_all(self) -> list[Product]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, product_id: int) -> Product | None:
        raise NotImplementedError

    @abstractmethod
    async def save(self, product: Product) -> None:
        raise NotImplementedError
