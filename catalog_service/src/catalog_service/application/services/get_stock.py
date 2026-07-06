from catalog_service.src.catalog_service.application.ports.product_repo import ProductRepository


class GetStockUserCase:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    async def get_stock(self, product_id: int) -> int:
        product = await self.repo.get_by_id(product_id)

        if product is None:
            raise ValueError(f'Product with ID {product_id} not found')  # TODO: Заменить на кастомную ошибку

        return product.stock
