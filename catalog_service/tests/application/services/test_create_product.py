import pytest

from catalog_service.domain.entities.product import Product
from catalog_service.tests.application.services.conftest import create_product_use_case


@pytest.mark.asyncio
async def test_create_product(create_product_use_case):
    """Тестирование сохранения продукта в БД"""
    product = await create_product_use_case.execute(name='Вода дистиллированная', price=50)
    assert isinstance(product, Product)
    assert product.id is not None
