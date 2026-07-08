import re
from dataclasses import dataclass

EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        if not EMAIL_PATTERN.match(self.value):
            raise ValueError('Invalid email format')
