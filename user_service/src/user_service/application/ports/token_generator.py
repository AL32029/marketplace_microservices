from abc import ABC, abstractmethod


class TokenGeneratorRepo(ABC):
    @abstractmethod
    def encode_token(self, sub: dict, exp: int = 3600) -> str:
        """Генерация токена"""
        raise NotImplemented

    @abstractmethod
    def decode_token(self, token: str) -> dict:
        """Расшифровка токена"""
        raise NotImplemented
