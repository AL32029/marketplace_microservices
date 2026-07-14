
from catalog_service.application.ports.product_repo import ProductRepository
from catalog_service.domain.entities.product import Product


class GetAllProductsUseCase:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    async def get_all_products(self) -> list[Product]:
        return await self.repo.get_all()
