import pytest

from catalog_service.domain.entities.product import Product
from catalog_service.domain.exceptions.catalog_errors import InsufficientStockError, NegativeQuantityError


def test_product_reduce_stock():
    """Тестирование метода reduce_stock"""
    product = Product(id=1, name='Вода дистиллированная', price=50, stock=5)
    product.reduce_stock(3)
    assert product.stock == 2


def test_product_reduce_raises_if_stock_negative():
    """Тестирование ошибки вызова reduce_stock с отрицательным количеством"""
    product = Product(id=1, name='Вода дистиллированная', price=50, stock=5)

    with pytest.raises(NegativeQuantityError):
        product.reduce_stock(-5)


def test_product_reduce_raises_if_stock_insufficient():
    """Тестирование ошибки вызова reduce_stock с количеством, превышающем запасы"""
    product = Product(id=1, name='Вода дистиллированная', price=50, stock=5)

    with pytest.raises(InsufficientStockError):
        product.reduce_stock(10)


def test_product_increase_stock():
    """Тестирование метода increase_stock"""
    product = Product(id=1, name='Вода дистиллированная', price=50, stock=5)

    product.increase_stock(10)
    assert product.stock == 15


def test_product_increase_raises_if_stock_negative():
    """Тестирование ошибки вызова increase_stock с отрицательным количеством"""
    product = Product(id=1, name='Вода дистиллированная', price=50, stock=5)

    with pytest.raises(NegativeQuantityError):
        product.increase_stock(-5)
