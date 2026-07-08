from dataclasses import dataclass

from user_service.domain.exceptions.user_errors import PasswordValidationError


@dataclass(frozen=True)
class Password:
    value: str

    def __post_init__(self):
        if len(self.value) < 8:
            raise PasswordValidationError('The password must be at least 8 characters long')
