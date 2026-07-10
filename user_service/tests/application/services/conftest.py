import pytest
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from user_service.application.services.login_user import LoginUserUseCase
from user_service.application.services.register_user import RegisterUserUseCase
from user_service.domain.entities.user import User
from user_service.infrastructure.db.models import Base
from user_service.infrastructure.repositories.bcrypt_password_hasher_repo import BCryptPasswordHasherRepo
from user_service.infrastructure.repositories.jwt_token_generator import JWTTokenGeneratorRepo
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
async def jwt_token_repo():
    return JWTTokenGeneratorRepo('test', 'HS256')


@pytest.fixture
async def login_user_use_case(user_repo, password_hasher_repo, jwt_token_repo):
    return LoginUserUseCase(user_repo, password_hasher_repo, jwt_token_repo)


@pytest.fixture
async def register_user_use_case(user_repo, password_hasher_repo):
    return RegisterUserUseCase(user_repo, password_hasher_repo)


@pytest.fixture
async def user_orm_item(register_user_use_case) -> User:
    user = await register_user_use_case.execute(email='user@example.com', full_name='Иванов Иван', password='123456789')
    return user
