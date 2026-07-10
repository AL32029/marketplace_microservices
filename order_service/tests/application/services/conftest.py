import pytest
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from order_service.domain.entities.order import Order, OrderItem
from order_service.infrastructure.db.models import Base
from order_service.infrastructure.repositories.sqlalchemy_order_repo import SQLAlchemyOrderRepo


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
    return SQLAlchemyOrderRepo(async_session_fixture)


@pytest.fixture
def order_item():
    return Order(user_id=1, items=[OrderItem(product_id=1, quantity=2, price=10.0)])
