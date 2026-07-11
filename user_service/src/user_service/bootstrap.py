from sqlalchemy.ext.asyncio import AsyncSession

from user_service.application.ports.password_hasher_repo import PasswordHasherRepo
from user_service.application.ports.token_generator import TokenGeneratorRepo
from user_service.application.services import GetProfileUseCase, LoginUserUseCase, RegisterUserUseCase
from user_service.infrastructure.config import JWTSettings
from user_service.infrastructure.repositories import BCryptPasswordHasherRepo, JWTTokenGeneratorRepo, SQLAlchemyUserRepo


def build_services(jwt_settings: JWTSettings) -> dict:
    async def password_hasher_repo():
        return BCryptPasswordHasherRepo()

    async def register_user_use_case(session: AsyncSession, password_repo: PasswordHasherRepo):
        return RegisterUserUseCase(SQLAlchemyUserRepo(session), password_repo)

    async def login_user_use_case(
            session: AsyncSession, password_repo: PasswordHasherRepo, jwt_token_repo: TokenGeneratorRepo
    ):
        return LoginUserUseCase(SQLAlchemyUserRepo(session), password_repo, jwt_token_repo)

    async def get_profile_use_case(session: AsyncSession):
        return GetProfileUseCase(SQLAlchemyUserRepo(session))

    async def jwt_token_generator_repo():
        return JWTTokenGeneratorRepo(jwt_settings.SECRET_KEY, jwt_settings.ALGORITHM)

    return {
        'password_hasher_repo': password_hasher_repo,
        'register_user_use_case': register_user_use_case,
        'login_user_use_case': login_user_use_case,
        'get_profile_use_case': get_profile_use_case,
        'jwt_token_generator_repo': jwt_token_generator_repo,
    }
