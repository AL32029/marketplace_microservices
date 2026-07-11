from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from user_service.application.ports.password_hasher_repo import PasswordHasherRepo
from user_service.application.services import RegisterUserUseCase
from user_service.presentation.dependencies import get_db, password_hasher_repo_depends


async def register_user_use_case_depends(
        request: Request,
        session: AsyncSession = Depends(get_db),
        password_hasher: PasswordHasherRepo = Depends(password_hasher_repo_depends)
) -> RegisterUserUseCase:
    factory = request.app.state.services['register_user_use_case']
    return await factory(session, password_hasher)
