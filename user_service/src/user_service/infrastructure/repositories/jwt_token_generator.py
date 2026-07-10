import datetime

from jose import jwt, JWTError

from user_service.application.ports.token_generator import TokenGeneratorRepo
from user_service.domain.exceptions.user_errors import InvalidJWTTokenError, JWTTokenExpiredError, \
    InvalidJWTTokenSubError


class JWTTokenGeneratorRepo(TokenGeneratorRepo):
    def __init__(self, secret_key: str, algorithm: str):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def encode_token(self, sub: dict, expires_in: int = 3600) -> str:
        sub['expires_to'] = (datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=expires_in)).timestamp()

        token = jwt.encode(sub, self.secret_key, self.algorithm)

        return token

    def decode_token(self, token: str) -> dict:
        try:
            sub = jwt.decode(token, self.secret_key, self.algorithm)
        except JWTError:
            raise InvalidJWTTokenError('Invalid JWT token')

        if 'expires_to' not in sub:
            raise InvalidJWTTokenSubError('The JWT token data does not have an expires_to field')

        if sub['expires_to'] < datetime.datetime.now(datetime.UTC).timestamp():
            raise JWTTokenExpiredError('The validity period of the JWT token has expired')

        return sub
