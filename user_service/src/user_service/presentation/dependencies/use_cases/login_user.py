from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from user_service.application.services.login_user import LoginUserUseCase
from user_service.infrastructure.repositories.bcrypt_password_hasher_repo import BCryptPasswordHasherRepo
from user_service.infrastructure.repositories.jwt_token_generator import JWTTokenGeneratorRepo
from user_service.presentation.dependencies.db.get_db_session import get_db
from user_service.presentation.dependencies.use_cases.jwt_token_generator import jwt_token_generator_repo_depends
from user_service.presentation.dependencies.use_cases.password_hasher import password_hasher_repo_depends


async def login_user_use_case_depends(
        request: Request,
        session: AsyncSession = Depends(get_db),
        password_hasher: BCryptPasswordHasherRepo = Depends(password_hasher_repo_depends),
        jwt_token_generator: JWTTokenGeneratorRepo = Depends(jwt_token_generator_repo_depends)
) -> LoginUserUseCase:
    factory = request.app.state.services['login_user_use_case']
    return await factory(session, password_hasher, jwt_token_generator)
