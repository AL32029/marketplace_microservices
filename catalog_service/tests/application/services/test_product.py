import pytest
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from catalog_service.domain.entities.product import Product
from catalog_service.infrastructure.db.models import Base
from catalog_service.infrastructure.repositories.sqlalchemy_project_repo import SQLAlchemyProductRepo


@pytest.fixture
async def async_session_fixture(tmp_path):
    db_file = tmp_path / "test.db"
    engine = create_async_engine(
        f"sqlite+aiosqlite:///{db_file}",
        poolclass=NullPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        yield session

    await engine.dispose()


@pytest.fixture
async def product_repo(async_session_fixture):
    return SQLAlchemyProductRepo(async_session_fixture)


@pytest.fixture
def product_item():
    return Product(id=1, name='Вода дистиллированная', price=50, stock=5)


@pytest.mark.asyncio
async def test_create_product_save(product_repo, product_item):
    """Тестирование сохранения товара"""
    await product_repo.save(product_item)
    assert product_item.id is not None


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
    with pytest.raises(ValueError):
        product_item.reduce_stock(10)


def test_product_increase_stock(product_item):
    """Тестирование метода increase_stock"""
    product_item.increase_stock(10)
    assert product_item.stock == 15


def test_product_increase_raises_if_stock_negative(product_item):
    """Тестирование ошибки вызова increase_stock с отрицательным количеством"""
    with pytest.raises(ValueError):
        product_item.increase_stock(-5)
