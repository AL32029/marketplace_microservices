from sqlalchemy.ext.asyncio import AsyncSession

from user_service.application.services.get_profile import GetProfileUseCase
from user_service.application.services.login_user import LoginUserUseCase
from user_service.application.services.register_user import RegisterUserUseCase
from user_service.infrastructure.repositories.bcrypt_password_hasher_repo import BCryptPasswordHasherRepo
from user_service.infrastructure.repositories.sqlalchemy_user_repo import SQLAlchemyUserRepo


def build_services() -> dict:
    async def password_hasher_repo():
        return BCryptPasswordHasherRepo()

    async def register_user_use_case(session: AsyncSession, password_repo: BCryptPasswordHasherRepo):
        return RegisterUserUseCase(SQLAlchemyUserRepo(session), password_repo)

    async def login_user_use_case(session: AsyncSession, password_repo: BCryptPasswordHasherRepo):
        return LoginUserUseCase(SQLAlchemyUserRepo(session), password_repo)

    async def get_profile_use_case(session: AsyncSession):
        return GetProfileUseCase(SQLAlchemyUserRepo(session))

    return {
        'password_hasher_repo': password_hasher_repo,
        'register_user_use_case': register_user_use_case,
        'login_user_use_case': login_user_use_case,
        'get_profile_use_case': get_profile_use_case,
    }
