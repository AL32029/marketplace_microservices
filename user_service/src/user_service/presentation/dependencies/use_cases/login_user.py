from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from user_service.application.services.login_user import LoginUserUseCase
from user_service.infrastructure.repositories.bcrypt_password_hasher_repo import BCryptPasswordHasherRepo
from user_service.presentation.dependencies import get_db, password_hasher_use_case_depends


async def login_user_use_case_depends(
        request: Request,
        session: AsyncSession = Depends(get_db),
        password_hasher: BCryptPasswordHasherRepo = Depends(password_hasher_use_case_depends)
) -> LoginUserUseCase:
    factory = request.app.state.services['login_user_use_case']
    return await factory(session, password_hasher)
