import asyncio
import os
import subprocess
import sys

import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from testcontainers.postgres import PostgresContainer

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer('postgres:17') as postgres:
        db_url = postgres.get_connection_url(driver='asyncpg')
        os.environ["TEST_DATABASE_URL"] = db_url
        subprocess.run(
            ["alembic", "-c", "alembic.ini", "upgrade", "head"],
            check=True,
            env=os.environ,
        )
        yield postgres


@pytest_asyncio.fixture(scope="function")
async def async_engine(postgres_container):
    engine = create_async_engine(
        os.environ["TEST_DATABASE_URL"],
        echo=False,
        pool_size=5,
        pool_pre_ping=True,
    )
    yield engine
    await engine.dispose()


async def _truncate_all_tables(async_engine):
    async with async_engine.connect() as conn:
        await conn.execute(text("SET session_replication_role = 'replica';"))
        result = await conn.execute(text(
            "SELECT tablename FROM pg_tables WHERE schemaname = 'public' "
            "AND tablename != 'alembic_version';"
        ))
        tables = [row[0] for row in result]
        for table in tables:
            await conn.execute(text(f'TRUNCATE TABLE "{table}" RESTART IDENTITY CASCADE;'))
        await conn.execute(text("SET session_replication_role = 'origin';"))
        await conn.commit()


@pytest_asyncio.fixture(scope="function")
async def async_session(async_engine):
    await _truncate_all_tables(async_engine)

    async_session_maker = async_sessionmaker(
        async_engine,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
    async with async_session_maker() as session:
        yield session