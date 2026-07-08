import datetime

from user_service.domain.entities.user import User
from user_service.domain.value_objects.email import Email
from user_service.domain.value_objects.password import Password


def test_user_change_password():
    """Тестирование функции change_password"""
    old_hash = "hashed_old_password"
    user = User(
        id=1,
        email=Email("user@example.com"),
        full_name="Иванов Иван",
        password_hash=Password(old_hash),
        role="user",
        created_at=datetime.datetime.now()
    )

    new_hash = "hashed_new_password"
    user.change_password(new_hash)

    assert user.password_hash.value == new_hash


def test_user_update_profile():
    """Тестирование функции update_profile"""
    user = User(
        id=1,
        email=Email("user@example.com"),
        full_name="Иванов Иван",
        password_hash=Password("hashed_password"),
        role="user",
        created_at=datetime.datetime.now()
    )
    user.update_profile('Петров Петр')
    assert user.full_name == 'Петров Петр'
