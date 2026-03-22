"""
Auth schemas for request/response validation
"""
from datetime import datetime
from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    email: str
    password: str = Field(..., min_length=8, description="Minimum 8 characters")


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    email: str
    is_premium: bool
    tier: str = "free"  # free, pro, pro_plus


class UserResponse(BaseModel):
    id: int
    email: str
    is_premium: bool
    tier: str = "free"  # free, pro, pro_plus
    created_at: datetime

    class Config:
        from_attributes = True


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8, description="Minimum 8 characters")
