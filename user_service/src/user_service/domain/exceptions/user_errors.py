class UserServiceError(BaseException):
    """Базовое исключение User Service"""
    pass


class InvalidUserLoginData(UserServiceError):
    """Ошибка логина (неверный логин или пароль)"""
    pass


class EmailValidationError(UserServiceError):
    """Ошибка валидации e-mail"""
    pass


class PasswordValidationError(UserServiceError):
    """Ошибка валидации пароля"""
    pass
