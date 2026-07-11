import pytest

from user_service.application.services import GetProfileUseCase


@pytest.fixture
async def get_profile_repo_use_case(user_repo):
    return GetProfileUseCase(user_repo)


async def test_get_profile_by_id(user_orm_item, get_profile_repo_use_case):
    """Тестирование вывода профиля в функции get_by_id"""
    user = await get_profile_repo_use_case.get_by_id(1)
    assert user is not None
    assert user == user_orm_item


async def test_get_profile_by_id_not_found(get_profile_repo_use_case):
    """Тестирование вывода None в функции get_by_id при неизвестном ID"""
    user = await get_profile_repo_use_case.get_by_id(2)
    assert user is None


async def test_get_profile_by_email(user_orm_item, get_profile_repo_use_case):
    """Тестирование вывода профиля в функции get_by_email"""
    user = await get_profile_repo_use_case.get_by_email('user@example.com')
    assert user is not None
    assert user == user_orm_item


async def test_get_profile_by_email_not_found(get_profile_repo_use_case):
    """Тестирование вывода None в функции get_by_email при неизвестном e-mail"""
    user = await get_profile_repo_use_case.get_by_email('not_user@example.com')
    assert user is None
