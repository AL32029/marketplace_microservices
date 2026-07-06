from abc import ABC, abstractmethod


class CatalogClient(ABC):
    @abstractmethod
    async def check_stock(self, product_id: int, quantity: int) -> bool:
        """Возвращает True, если товар есть в нужном количестве"""
        raise NotImplemented
