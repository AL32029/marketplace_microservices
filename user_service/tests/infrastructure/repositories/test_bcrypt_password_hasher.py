import pytest

from user_service.infrastructure.repositories.bcrypt_password_hasher_repo import BCryptPasswordHasherRepo


@pytest.fixture
def bcrypt_password_hasher_repo():
    return BCryptPasswordHasherRepo()


def test_hash_and_check_password(bcrypt_password_hasher_repo):
    password = 'test_hash_and_check_password'

    password_hash = bcrypt_password_hasher_repo.hash_password(password)

    assert bcrypt_password_hasher_repo.check_password(password, password_hash)
