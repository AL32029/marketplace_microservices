import datetime

import pytest

from user_service.domain.entities.user import User
from user_service.domain.value_objects.email import Email


@pytest.fixture
def user_item():
    return User(
        id=1,
        email=Email('user@example.com'),
        full_name='Иванов Иван',
        password_hash='123123',
        role='user',
        created_at=datetime.datetime.now()
    )


def test_user_change_password(user_item):
    """Тестирование функции change_password"""
    user_item.change_password('123456789')
    assert user_item.password_hash.value == '123456789'


def test_user_update_profile(user_item):
    """Тестирование функции update_profile"""
    user_item.update_profile('Петров Петр')
    assert user_item.full_name == 'Петров Петр'
