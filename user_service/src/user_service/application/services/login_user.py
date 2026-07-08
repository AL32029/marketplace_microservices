from user_service.application.ports.password_hasher_repo import PasswordHasherRepo
from user_service.application.ports.user_repo import UserRepository
from user_service.domain.exceptions.user_errors import InvalidUserLoginData


class LoginUserUseCase:
    def __init__(self, user_repo: UserRepository, password_hasher_repo: PasswordHasherRepo):
        self.user_repo = user_repo
        self.password_hasher_repo = password_hasher_repo

    async def login(self, email: str, password: str):
        user = await self.user_repo.get_by_email(email)

        if user is None:
            raise InvalidUserLoginData('Invalid email or password') # [MISC][DONE] Реализовать кастомную ошибку

        password_is_valid = self.password_hasher_repo.check_password(password, user.password_hash.value)

        if not password_is_valid:
            raise InvalidUserLoginData('Invalid email or password') # [MISC][DONE] Реализовать кастомную ошибку

        return user # TODO: Переделать на выдачу JWT токена