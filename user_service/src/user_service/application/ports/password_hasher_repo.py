from abc import ABC, abstractmethod


class PasswordHasherRepo(ABC):
    @abstractmethod
    def hash_password(self, password: str) -> str:
        """Хэширование пароля"""
        raise NotImplemented

    @abstractmethod
    def check_password(self, password: str, password_hash: str) -> bool:
        """Проверка пароля"""
        raise NotImplemented
