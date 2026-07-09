from pydantic import BaseModel

from user_service.domain.value_objects.email import Email
from user_service.domain.value_objects.password import Password


class UserRegisterSchema(BaseModel):
    email: Email
    password: Password
    full_name: str


class UserLoginSchema(BaseModel):
    email: Email
    password: Password

class UserProfileResponse(BaseModel):
    id: int
    email: Email
    full_name: str
    role: str