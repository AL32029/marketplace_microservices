import pytest
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from catalog_service.application.services.create_product import CreateProductUseCase
from catalog_service.application.services.reserve_stock import ReserveStockUseCase
from catalog_service.domain.exceptions.catalog_errors import ProductNotFoundError, InsufficientStockError
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
async def create_product_use_case(product_repo):
    return CreateProductUseCase(product_repo)


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
