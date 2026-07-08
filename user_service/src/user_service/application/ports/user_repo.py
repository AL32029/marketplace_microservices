from abc import ABC, abstractmethod
from typing import Optional

from user_service.domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Получение профиля пользователя по Email"""
        raise NotImplemented

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Получение профиля пользователя по ID"""
        raise NotImplemented

    @abstractmethod
    async def save(self, user: User) -> None:
        """Создание/обновление пользователя в БД"""
        raise NotImplemented
