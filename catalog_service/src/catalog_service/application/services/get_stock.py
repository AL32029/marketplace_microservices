from catalog_service.application.ports.product_repo import ProductRepository
from catalog_service.domain.exceptions.catalog_errors import ProductNotFoundError


class GetStockUseCase:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    async def get_stock(self, product_id: int) -> int:
        product = await self.repo.get_by_id(product_id)

        if product is None:
            raise ProductNotFoundError(f'Product with ID {product_id} not found')

        return product.stock
