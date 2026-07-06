from catalog_service.application.ports.product_repo import ProductRepository


class ReserveStockUseCase:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    async def reserve_stock(self, product_id: int, quantity: int) -> None:
        product = await self.repo.get_by_id(product_id)

        if product is None:
            raise ValueError(f'Product with ID {product_id} not found')  # TODO: Заменить на кастомную ошибку

        product.reduce_stock(quantity)
        await self.repo.save(product)
