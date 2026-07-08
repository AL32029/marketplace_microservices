from typing import Optional

from user_service.application.ports.user_repo import UserRepository
from user_service.domain.entities.user import User


class GetProfileUseCase:
    def __init__(self, user_repo: UserRepository):
        self.repo = user_repo

    async def get_by_id(self, user_id: int) -> Optional[User]:
        user = await self.repo.get_by_id(user_id)

        if user is None:
            return None  

        return user

    async def get_by_email(self, email: str) -> Optional[User]:
        user = await self.repo.get_by_email(email)

        if user is None:
            return None  

        return user
