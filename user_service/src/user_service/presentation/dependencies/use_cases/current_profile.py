from typing import Optional

from fastapi import Depends, HTTPException, Request

from user_service.application.ports.token_generator import TokenGeneratorRepo
from user_service.application.ports.user_repo import UserRepository
from user_service.domain.entities.user import User
from user_service.domain.exceptions.user_errors import JWTTokenExpiredError, InvalidJWTTokenSubError
from user_service.presentation.dependencies.use_cases.get_profile import get_profile_use_case_depends
from user_service.presentation.dependencies.use_cases.jwt_token_generator import jwt_token_generator_repo_depends


async def get_current_user(
        request: Request,
        token_repo: TokenGeneratorRepo = Depends(jwt_token_generator_repo_depends),
        user_repo: UserRepository = Depends(get_profile_use_case_depends)
) -> User:
    try:
        auth_info = request.headers.get('Authentication')

        if not auth_info:
            raise HTTPException(status_code=401, detail='Authentication is required')

        auth_info = auth_info.strip()

        if len(auth_info) != 2:
            raise HTTPException(status_code=401, detail='Invalid authentication info')

        auth_type, auth_token = auth_info

        if auth_type.lower() != 'bearer':
            raise HTTPException(status_code=401, detail='Invalid authentication method')

        payload = token_repo.decode_token(auth_token)
        user_id: Optional[int] = payload.get('id')

        if not user_id:
            raise HTTPException(status_code=401, detail='Invalid token')

        user = await user_repo.get_by_id(user_id)

        if user is None:
            raise HTTPException(status_code=404, detail='User not found')

        return user
    except (JWTTokenExpiredError, InvalidJWTTokenSubError):
        raise HTTPException(401, "Invalid or expired token")
