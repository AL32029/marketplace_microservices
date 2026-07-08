import pytest

from catalog_service.application.services.reserve_stock import ReserveStockUseCase
from catalog_service.domain.exceptions.catalog_errors import ProductNotFoundError, InsufficientStockError


@pytest.fixture
async def reserve_stock_use_case(product_repo):
    return ReserveStockUseCase(product_repo)


@pytest.fixture
async def product_item(product_repo, create_product_use_case):
    product = await create_product_use_case.execute(name='Вода дистиллированная', price=50)
    product.stock = 50
    await product_repo.save(product)
    return product


async def test_reserve_stock(reserve_stock_use_case, product_repo, product_item):
    """Тестирование бронирования товара"""
    await reserve_stock_use_case.reserve_stock(product_item.id, 20)
    product_item = await product_repo.get_by_id(product_item.id)
    assert product_item.stock == 30


async def test_get_stock_error_not_found(reserve_stock_use_case):
    """Тестирование ошибки при бронировании отсутствующего товара"""
    with pytest.raises(ProductNotFoundError):
        await reserve_stock_use_case.reserve_stock(2, 20)


async def test_get_stock_error_insufficient_stock_error(reserve_stock_use_case, product_item):
    """Тестирование ошибки при бронировании товара, запасы которого меньше бронируемого количества"""
    with pytest.raises(InsufficientStockError):
        await reserve_stock_use_case.reserve_stock(product_item.id, 100)
