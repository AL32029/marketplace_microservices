from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from user_service.application.services.login_user import LoginUserUseCase
from user_service.application.services.register_user import RegisterUserUseCase
from user_service.domain.entities.user import User
from user_service.domain.exceptions.user_errors import (EmailValidationError, PasswordValidationError, UniqueEmailError,
                                                        InvalidUserLoginData)
from user_service.presentation.dependencies import (register_user_use_case_depends, login_user_use_case_depends,
                                                    )
from user_service.presentation.dependencies.use_cases.current_profile import get_current_user
from user_service.presentation.mappers.user_mapper import domain_to_response
from user_service.presentation.schemas.user_schema import UserRegisterSchema, UserLoginSchema, TokenResponse, \
    UserProfileResponse

router = APIRouter()


@router.post('/auth/register', response_model=UserProfileResponse)
async def register_user(
        register_data: UserRegisterSchema, use_case: RegisterUserUseCase = Depends(register_user_use_case_depends)
):
    try:
        user = await use_case.execute(
            register_data.email,
            register_data.full_name,
            register_data.password
        )
    except (EmailValidationError, PasswordValidationError) as e:
        raise HTTPException(status_code=422, detail=f'Data validation error: {e}')
    except UniqueEmailError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return domain_to_response(user)


@router.post(
    '/auth/login',
    response_model=TokenResponse,
    openapi_extra={
        "requestBody": {
            "content": {
                "application/x-www-form-urlencoded": {
                    "schema": UserLoginSchema.model_json_schema()
                }
            }
        }
    }
)
async def login_user(
        login_data: OAuth2PasswordRequestForm = Depends(),
        login_use_case: LoginUserUseCase = Depends(login_user_use_case_depends)
):
    # [MISC][DONE] Реализовать эндпоинт login_user
    try:
        token = await login_use_case.login(email=login_data.username, password=login_data.password)
    except InvalidUserLoginData as e:
        raise HTTPException(status_code=403, detail=str(e))

    return TokenResponse(access_token=token)  # [MISC][DONE] Переделать на выдачу токена


@router.get('/users/me', response_model=UserProfileResponse)
async def get_user_profile(
        user: User = Depends(get_current_user)
):
    # [MISC][DONE] Реализовать эндпоинт get_user_profile
    return domain_to_response(user)
