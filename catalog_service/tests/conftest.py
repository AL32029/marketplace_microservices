import pytest
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from catalog_service.infrastructure.db.models import Base
from catalog_service.infrastructure.repositories.sqlalchemy_product_repo import SQLAlchemyProductRepo


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
