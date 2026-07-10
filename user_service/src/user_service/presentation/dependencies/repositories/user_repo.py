from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from user_service.application.ports.user_repo import UserRepository
from user_service.infrastructure.repositories.sqlalchemy_user_repo import SQLAlchemyUserRepo
from user_service.presentation.dependencies.db.get_db_session import get_db


async def user_repo_depends(session: AsyncSession = Depends(get_db)) -> UserRepository:
    return SQLAlchemyUserRepo(session)