import datetime
from dataclasses import dataclass
from typing import Optional

from user_service.domain.value_objects.email import Email
from user_service.domain.value_objects.password import Password


@dataclass
class User:
    email: Email
    password_hash: Password
    full_name: str
    role: str

    id: Optional[int] = None
    created_at: Optional[datetime.datetime] = None

    def change_password(self, new_password: str):
        self.password_hash = Password(new_password)

    def update_profile(self, full_name: str):
        self.full_name = full_name
