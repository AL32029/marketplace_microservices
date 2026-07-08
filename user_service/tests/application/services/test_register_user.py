import pytest

from user_service.domain.exceptions.user_errors import EmailValidationError, PasswordValidationError


async def test_register_user(register_user_use_case):
    user = await register_user_use_case.execute(
        email='user@example.com',
        full_name='Иванов Иван',
        password='123456789'
    )
    assert user.id is not None


async def test_register_user_error_invalid_email(register_user_use_case):
    with pytest.raises(EmailValidationError):
        await register_user_use_case.execute(
            email='userexample.com',
            full_name='Иванов Иван',
            password='123456789'
        )


async def test_register_user_error_short_password(register_user_use_case):
    with pytest.raises(PasswordValidationError):
        await register_user_use_case.execute(
            email='user@example.com',
            full_name='Иванов Иван',
            password='123123'
        )
