from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from user_service.application.services.register_user import RegisterUserUseCase
from user_service.infrastructure.repositories.bcrypt_password_hasher_repo import BCryptPasswordHasherRepo
from user_service.presentation.dependencies import get_db, password_hasher_use_case_depends


async def register_user_use_case_depends(
        request: Request,
        session: AsyncSession = Depends(get_db),
        password_hasher: BCryptPasswordHasherRepo = Depends(password_hasher_use_case_depends)
) -> RegisterUserUseCase:
    factory = request.app.state.services['register_user_use_case']
    return await factory(session, password_hasher)
