import pytest
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from catalog_service.application.services.create_product import CreateProductUseCase
from catalog_service.application.services.get_stock import GetStockUseCase
from catalog_service.domain.entities.product import Product
from catalog_service.domain.exceptions.catalog_errors import ProductNotFoundError
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
