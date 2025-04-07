from pydantic import BaseModel, EmailStr, field_validator

class UserBase(BaseModel):
    email: EmailStr

    @field_validator("email")
    def sanitize_email(cls, value):
        return value.lower()

class UserCreate(UserBase):
    password: str
    class Config:
        from_attributes: True

class User(UserBase):
    id: int | None
    class Config:
        from_attributes = True


class LoginCredentials(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"