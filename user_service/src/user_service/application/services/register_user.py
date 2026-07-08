from user_service.application.ports.password_hasher_repo import PasswordHasherRepo
from user_service.application.ports.user_repo import UserRepository
from user_service.domain.entities.user import User
from user_service.domain.value_objects.email import Email
from user_service.domain.value_objects.password import Password


class RegisterUserUseCase:
    def __init__(self, user_repo: UserRepository, password_hasher_repo: PasswordHasherRepo):
        self.user_repo = user_repo
        self.password_hasher_repo = password_hasher_repo

    async def execute(self, email: str, full_name: str, password: str) -> User:
        password_domain = Password(password)
        password_hash = await self.password_hasher_repo.hash_password(password_domain.value)
        user = User(
            email=Email(email),
            password_hash=password_hash,
            full_name=full_name,
            role='user'
        )

        await self.user_repo.save(user)

        return user
