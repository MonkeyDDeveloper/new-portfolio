from pydantic import BaseModel
from typing import Optional

class AuthResponse(BaseModel):
    success: bool
    message: str
    token: Optional[str]

class UserInDB(BaseModel):
    username: str
    password: str

class FindUserResponse(BaseModel):
    success: bool
    message: str
    user: Optional[UserInDB]

class ApiUser(BaseModel):
    username: str
    email: str
    password: str

class TokenRequest(BaseModel):
    api_user: ApiUser