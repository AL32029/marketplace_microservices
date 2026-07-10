from pydantic import BaseModel, EmailStr


class UserRegisterSchema(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserProfileResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'
