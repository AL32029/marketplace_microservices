from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from user_service.application.ports.token_generator import TokenGeneratorRepo
from user_service.application.ports.user_repo import UserRepository
from user_service.domain.entities.user import User
from user_service.domain.exceptions.user_errors import JWTTokenExpiredError, InvalidJWTTokenSubError
from user_service.presentation.dependencies.repositories.jwt_token_generator import jwt_token_generator_repo_depends
from user_service.presentation.dependencies.repositories.user_repo import user_repo_depends

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        token_repo: TokenGeneratorRepo = Depends(jwt_token_generator_repo_depends),
        user_repo: UserRepository = Depends(user_repo_depends)
) -> User:
    try:
        payload = token_repo.decode_token(token)
        user_id: Optional[int] = payload.get('id')

        if not user_id:
            raise HTTPException(status_code=401, detail='Invalid token')

        user = await user_repo.get_by_id(user_id)

        if user is None:
            raise HTTPException(status_code=404, detail='User not found')

        return user
    except (JWTTokenExpiredError, InvalidJWTTokenSubError):
        raise HTTPException(401, "Invalid or expired token")
