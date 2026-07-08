import pytest

from catalog_service.domain.entities.product import Product


@pytest.fixture
def product_item():
    return Product(id=1, name='Вода дистиллированная', price=50, stock=5)


@pytest.fixture
async def product_from_repo(product_repo, product_item):
    await product_repo.save(product_item)
    return product_item


@pytest.mark.asyncio
async def test_create_product_save(product_repo, product_item):
    """Тестирование сохранения товара"""
    await product_repo.save(product_item)
    assert product_item.id is not None


@pytest.mark.asyncio
async def test_get_product_by_id(product_repo, product_from_repo):
    """Тестирование получения продукта"""
    result = await product_repo.get_by_id(product_from_repo.id)
    assert result == product_from_repo


@pytest.mark.asyncio
async def test_get_product_by_id_not_found(product_repo, product_from_repo):
    """Тестирование получения None при отсутствии товара на складе"""
    result = await product_repo.get_by_id(2)
    assert result is None
