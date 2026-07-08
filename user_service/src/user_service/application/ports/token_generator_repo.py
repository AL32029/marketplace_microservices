from abc import ABC, abstractmethod


class TokenGeneratorRepo(ABC):
    @abstractmethod
    def encode_token(self, sub: dict) -> str:
        """Генерация JWT токена"""
        raise NotImplemented

    @abstractmethod
    def decode_token(self, token: str) -> str:
        """Расшифровка JWT токена"""
        raise NotImplemented
