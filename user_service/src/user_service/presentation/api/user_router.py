from fastapi import APIRouter, Depends, HTTPException

from user_service.application.services.login_user import LoginUserUseCase
from user_service.application.services.register_user import RegisterUserUseCase
from user_service.domain.exceptions.user_errors import EmailValidationError, PasswordValidationError, UniqueEmailError
from user_service.presentation.api.mappers.user_mapper import domain_to_response
from user_service.presentation.dependencies import register_user_use_case_depends, login_user_use_case_depends
from user_service.presentation.schemas.user_schema import UserRegisterSchema, UserLoginSchema

router = APIRouter()


@router.post('/auth/register')
async def register_user(
        register_data: UserRegisterSchema, use_case: RegisterUserUseCase = Depends(register_user_use_case_depends)
):
    try:
        user = await use_case.execute(
            register_data.email.value,
            register_data.full_name,
            register_data.password.value
        )
    except (EmailValidationError, PasswordValidationError) as e:
        raise HTTPException(status_code=422, detail=f'Data validation error: {e}')
    except UniqueEmailError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return domain_to_response(user)


@router.post('/auth/login')
async def login_user(login_data: UserLoginSchema, use_case: LoginUserUseCase = Depends(login_user_use_case_depends)):
    # TODO: Реализовать эндпонит login_user
    raise NotImplemented


@router.get('/users/me')
async def get_user_profile():
    # TODO: Реализовать эндпонит get_user_profile
    raise NotImplementedError
