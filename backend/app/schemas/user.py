"""User schemas."""
from typing import Optional
from datetime import datetime
from pydantic import EmailStr, Field, field_validator
from app.schemas.base import BaseSchema, BaseResponse


class UserBase(BaseSchema):
    """Base user schema."""
    
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    full_name: Optional[str] = Field(None, max_length=255)


class UserCreate(UserBase):
    """Schema for user creation."""
    
    password: str = Field(..., min_length=8, max_length=100)
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v


class UserUpdate(BaseSchema):
    """Schema for user update."""
    
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=255)


class UserResponse(BaseResponse, UserBase):
    """User response schema."""
    
    is_active: bool
    is_superuser: bool
    last_login: Optional[datetime] = None


class UserLogin(BaseSchema):
    """Schema for user login."""
    
    username: str
    password: str


class ChangePassword(BaseSchema):
    """Schema for changing password."""
    
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=100)
    
    @field_validator("new_password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v


class PasswordResetRequest(BaseSchema):
    """Schema for password reset request."""
    
    email: EmailStr


class PasswordResetConfirm(BaseSchema):
    """Schema for password reset confirmation."""
    
    token: str
    new_password: str = Field(..., min_length=8, max_length=100)
