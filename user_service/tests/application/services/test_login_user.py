import pytest

from user_service.domain.entities.user import User
from user_service.domain.exceptions.user_errors import InvalidUserLoginData
from user_service.tests.application.services.conftest import login_user_use_case


async def test_login_user(login_user_use_case, user_orm_item):
    """Тестирование авторизации пользователя при верных данных"""
    user = await login_user_use_case.login('user@example.com', '123456789')
    assert user is not None
    assert isinstance(user, User)


@pytest.mark.parametrize(
    'email,password',
    [
        ['not_user@example.com', '123456789'],
        ['user@example.com', '987654321'],
        ['not_user@example.com', '987654321'],
    ]
)
async def test_login_user_invalid_data(login_user_use_case, user_orm_item, email, password):
    """Тестирование ошибки авторизации при неверных данных"""
    with pytest.raises(InvalidUserLoginData) as e:
        await login_user_use_case.login(email, password)
        assert e == 'Invalid email or password'
