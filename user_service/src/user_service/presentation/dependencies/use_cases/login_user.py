from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from user_service.application.ports.password_hasher_repo import PasswordHasherRepo
from user_service.application.ports.token_generator import TokenGeneratorRepo
from user_service.application.services import LoginUserUseCase
from user_service.infrastructure.repositories import JWTTokenGeneratorRepo
from user_service.presentation.dependencies.db.get_db_session import get_db
from user_service.presentation.dependencies.repositories.jwt_token_generator import jwt_token_generator_repo_depends
from user_service.presentation.dependencies.repositories.password_hasher import password_hasher_repo_depends


async def login_user_use_case_depends(
        request: Request,
        session: AsyncSession = Depends(get_db),
        password_hasher: PasswordHasherRepo = Depends(password_hasher_repo_depends),
        jwt_token_generator: TokenGeneratorRepo = Depends(jwt_token_generator_repo_depends)
) -> LoginUserUseCase:
    factory = request.app.state.services['login_user_use_case']
    return await factory(session, password_hasher, jwt_token_generator)
