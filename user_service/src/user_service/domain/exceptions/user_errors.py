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


class UniqueEmailError(UserServiceError):
    """Ошибка уникальности Email"""
    pass


class InvalidJWTTokenError(UserServiceError):
    """Ошибка валидации JWT токена"""
    pass


class JWTTokenExpiredError(UserServiceError):
    """Ошибка истечения срока действия JWT токена"""
    pass

class InvalidJWTTokenSubError(UserServiceError):
    """Ошибка валидации sub JWT токена"""
    pass