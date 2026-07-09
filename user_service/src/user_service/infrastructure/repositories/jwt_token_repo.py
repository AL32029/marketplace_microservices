from jose import jwt

from user_service.application.ports.token_generator_repo import TokenGeneratorRepo


class JWTTokenGeneratorRepo(TokenGeneratorRepo):
    def __init__(self, secret_key: str, algorithm: str):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def encode_token(self, sub: dict) -> str:
        token = jwt.encode(sub, self.secret_key, self.algorithm)
        return token

    def decode_token(self, token: str) -> dict:
        # TODO: Добавить обработку ошибки при неверном токене
        sub = jwt.decode(token, self.secret_key, self.algorithm)
        return sub
