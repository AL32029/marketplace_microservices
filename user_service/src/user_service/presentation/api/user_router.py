from fastapi import APIRouter, Depends, HTTPException

from user_service.application.services.get_profile import GetProfileUseCase
from user_service.application.services.login_user import LoginUserUseCase
from user_service.application.services.register_user import RegisterUserUseCase
from user_service.domain.exceptions.user_errors import (EmailValidationError, PasswordValidationError, UniqueEmailError,
                                                        InvalidUserLoginData)
from user_service.presentation.api.mappers.user_mapper import domain_to_response
from user_service.presentation.dependencies import (register_user_use_case_depends, login_user_use_case_depends,
                                                    )
from user_service.presentation.dependencies.use_cases.get_profile import get_profile_use_case_depends
from user_service.presentation.schemas.user_schema import UserRegisterSchema, UserLoginSchema, TokenResponse

router = APIRouter()


@router.post('/auth/register')
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


@router.post('/auth/login')
async def login_user(
        login_data: UserLoginSchema,
        login_use_case: LoginUserUseCase = Depends(login_user_use_case_depends)
):
    # [MISC][DONE] Реализовать эндпоинт login_user
    try:
        token = await login_use_case.login(email=login_data.email, password=login_data.password)
    except InvalidUserLoginData as e:
        raise HTTPException(status_code=403, detail=str(e))

    return TokenResponse(access_token=token)  # [MISC][DONE] Переделать на выдачу токена


@router.get('/users/me')
async def get_user_profile(
        get_profile_use_case: GetProfileUseCase = Depends(get_profile_use_case_depends)
):
    # TODO: Реализовать эндпоинт get_user_profile
    raise NotImplementedError
