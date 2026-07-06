from catalog_service.src.catalog_service.application.ports.product_repo import ProductRepository
from catalog_service.src.catalog_service.domain.entities.product import Product


class CreateProductUseCase:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    async def execute(self, name: str, price: int) -> Product:
        product = Product(name, price)

        await self.product_repo.save(product)

        return product
