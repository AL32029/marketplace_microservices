from unittest.mock import AsyncMock

import pytest
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from order_service.application.services.create_order import CreateOrderUseCase
from order_service.domain.entities.order import Order, OrderItem
from order_service.infrastructure.db.models import Base
from order_service.infrastructure.repositories.sqlalchemy_order_repo import SQLALchemyOrderRepo


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
async def order_repo(async_session_fixture):
    return SQLALchemyOrderRepo(async_session_fixture)


@pytest.fixture
def order_item():
    return Order(user_id=1, items=[OrderItem(product_id=1, quantity=2, price=10.0)])


@pytest.mark.asyncio
async def test_create_order_saves_order(order_repo, order_item):
    """Тестирование сохранения заказа"""
    await order_repo.save(order_item)
    assert order_item.id is not None


@pytest.mark.asyncio
async def test_create_order_raises_if_stock_insufficient(order_item):
    """Тестирование отсутствия нужного количества товара на складе"""
    mock_repo = AsyncMock()
    mock_catalog = AsyncMock()
    mock_catalog.check_stock.return_value = False

    use_case = CreateOrderUseCase(mock_repo, mock_catalog)

    with pytest.raises(ValueError, match="insufficient stock"):
        await use_case.execute(
            user_id=order_item.user_id,
            items=order_item.items
        )

    mock_repo.save.assert_not_called()