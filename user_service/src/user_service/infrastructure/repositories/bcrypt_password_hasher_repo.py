import bcrypt

from user_service.application.ports.password_hasher_repo import PasswordHasherRepo


class BCryptPasswordHasherRepo(PasswordHasherRepo):
    def hash_password(self, password: str) -> str:
        password_encoded = password.encode('utf-8')

        salt = bcrypt.gensalt()

        password_hash = bcrypt.hashpw(password_encoded, salt)

        return password_hash.decode('utf-8')

    def check_password(self, password: str, password_hash: str) -> bool:
        password_encoded = password.encode('utf-8')
        password_hash_encoded = password_hash.encode('utf-8')

        return bcrypt.checkpw(password_encoded, password_hash_encoded)
