import pytest
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from user_service.application.services.register_user import RegisterUserUseCase
from user_service.infrastructure.db.models import Base
from user_service.infrastructure.repositories.bcrypt_password_hasher_repo import BCryptPasswordHasherRepo
from user_service.infrastructure.repositories.sqlalchemy_user_repo import SQLAlchemyUserRepo


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
async def user_repo(async_session_fixture):
    return SQLAlchemyUserRepo(async_session_fixture)


@pytest.fixture
async def password_hasher_repo():
    return BCryptPasswordHasherRepo()


@pytest.fixture
async def register_user_use_case(user_repo, password_hasher_repo):
    return RegisterUserUseCase(user_repo, password_hasher_repo)


@pytest.mark.asyncio
async def test_register_user(register_user_use_case):
    user = await register_user_use_case.execute(
        email='user@example.com',
        full_name='Иванов Иван',
        password='123456789'
    )
    assert user.id is not None


@pytest.mark.asyncio
async def test_register_user_error_invalid_email(register_user_use_case):
    with pytest.raises(ValueError):
        await register_user_use_case.execute(
            email='userexample.com',
            full_name='Иванов Иван',
            password='123456789'
        )


@pytest.mark.asyncio
async def test_register_user_error_short_password(register_user_use_case):
    with pytest.raises(ValueError):
        await register_user_use_case.execute(
            email='user@example.com',
            full_name='Иванов Иван',
            password='123123'
        )
