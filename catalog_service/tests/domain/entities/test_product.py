import pytest

from catalog_service.domain.entities.product import Product
from catalog_service.domain.exceptions.catalog_errors import InsufficientStockError


@pytest.fixture
def product_item():
    return Product(id=1, name='Вода дистиллированная', price=50, stock=5)


def test_product_reduce_stock(product_item):
    """Тестирование метода reduce_stock"""
    product_item.reduce_stock(3)
    assert product_item.stock == 2


def test_product_reduce_raises_if_stock_negative(product_item):
    """Тестирование ошибки вызова reduce_stock с отрицательным количеством"""
    with pytest.raises(ValueError):
        product_item.reduce_stock(-5)


def test_product_reduce_raises_if_stock_insufficient(product_item):
    """Тестирование ошибки вызова reduce_stock с количеством, превышающем запасы"""
    with pytest.raises(InsufficientStockError):
        product_item.reduce_stock(10)


def test_product_increase_stock(product_item):
    """Тестирование метода increase_stock"""
    product_item.increase_stock(10)
    assert product_item.stock == 15


def test_product_increase_raises_if_stock_negative(product_item):
    """Тестирование ошибки вызова increase_stock с отрицательным количеством"""
    with pytest.raises(ValueError):
        product_item.increase_stock(-5)
