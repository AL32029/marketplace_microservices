from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from user_service.application.services.get_profile import GetProfileUseCase
from user_service.presentation.dependencies.db.get_db_session import get_db


async def get_profile_use_case_depends(
        requests: Request, session: AsyncSession = Depends(get_db)
) -> GetProfileUseCase:
    factory = requests.app.state.services['get_profile_use_case']
    return await factory(session)
