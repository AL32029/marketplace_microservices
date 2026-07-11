import pytest

from user_service.application.services import LoginUserUseCase, RegisterUserUseCase
from user_service.domain.entities.user import User
from user_service.infrastructure.repositories import BCryptPasswordHasherRepo, JWTTokenGeneratorRepo, SQLAlchemyUserRepo
from user_service.tests.conftest import async_session_fixture


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
