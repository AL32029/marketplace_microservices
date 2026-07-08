from user_service.application.ports.password_hasher_repo import PasswordHasherRepo
from user_service.application.ports.user_repo import UserRepository


class LoginUserUseCase:
    def __init__(self, user_repo: UserRepository, password_hasher_repo: PasswordHasherRepo):
        self.user_repo = user_repo
        self.password_hasher_repo = password_hasher_repo

    async def login(self, email: str, password: str):
        user = await self.user_repo.get_by_email(email)

        if user is None:
            raise ValueError('Invalid email or password') # TODO: Реализовать кастомную ошибку

        password_hash = await self.password_hasher_repo.hash_password(password)

        if user.password_hash != password_hash:
            raise ValueError('Invalid email or password') # TODO: Реализовать кастомную ошибку

        return user # TODO: Переделать на выдачу JWT токена