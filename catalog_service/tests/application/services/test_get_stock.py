import pytest

from catalog_service.application.services.get_stock import GetStockUseCase
from catalog_service.domain.exceptions.catalog_errors import ProductNotFoundError


@pytest.fixture
async def get_stock_use_case(product_repo):
    return GetStockUseCase(product_repo)


@pytest.fixture
async def product_item(create_product_use_case):
    return await create_product_use_case.execute(name='Вода дистиллированная', price=50)


async def test_get_stock(get_stock_use_case, product_item):
    """Тестирование проверки остатков товара"""
    stock = await get_stock_use_case.get_stock(product_item.id)
    assert stock == 0


async def test_get_stock_error_not_found(get_stock_use_case):
    """Тестирование ошибки при проверке остатков отсутствующего товара"""
    with pytest.raises(ProductNotFoundError):
        await get_stock_use_case.get_stock(2)
