import pytest

from catalog_service.domain.entities.product import Product
from catalog_service.infrastructure.repositories.sqlalchemy_product_repo import (
    SQLAlchemyProductRepo,
)


@pytest.fixture(scope='function')
def product_repo(async_session):
    return SQLAlchemyProductRepo(async_session)


@pytest.fixture
def product_item():
    return Product(name='Вода дистиллированная', price=50, stock=5)


@pytest.fixture()
async def product_from_repo(product_repo, product_item) -> Product:
    await product_repo.save(product_item)
    return product_item


@pytest.mark.asyncio
async def test_create_product_save(product_repo, product_item):
    """SQLAlchemyProductRepo должен сохранить Product в базе данных и задать ему ID"""
    await product_repo.save(product_item)
    assert product_item.id is not None


@pytest.mark.asyncio
async def test_get_product_by_id(product_repo, product_from_repo):
    """SQLAlchemyProductRepo должен получить Product из базы данных по ID"""
    result = await product_repo.get_by_id(product_from_repo.id)
    assert result == product_from_repo


@pytest.mark.asyncio
async def test_get_product_by_id_not_found(product_repo):
    """SQLAlchemyProductRepo должен вернуть None"""
    result = await product_repo.get_by_id(999)
    assert result is None
