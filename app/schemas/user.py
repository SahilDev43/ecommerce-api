from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserCreate(BaseModel):
    first_name: str = Field(min_length=2, max_length=100)
    last_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length = 8)

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    is_active: bool
    role: str

    model_config = ConfigDict(from_attributes=True)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length = 8)

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length= 8)

class Token(BaseModel):
    access_token: str
    token_type: str