from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from user_service.application.ports.user_repo import UserRepository
from user_service.domain.entities.user import User
from user_service.domain.exceptions.user_errors import UniqueEmailError
from user_service.infrastructure.db.mappers import orm_to_domain, domain_to_orm
from user_service.infrastructure.db.models import UserORM


class SQLAlchemyUserRepo(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.session.get(UserORM, user_id)

        if result is None:
            return None

        return orm_to_domain(result)

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.scalar(select(UserORM).where(UserORM.email == email))

        if result is None:
            return None

        return orm_to_domain(result)

    async def save(self, user: User) -> None:
        orm_user = domain_to_orm(user)

        try:
            self.session.add(orm_user)
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise UniqueEmailError('The specified email address is already in use')

        user.id = orm_user.id
        user.created_at = orm_user.created_at
