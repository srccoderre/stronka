"""Base schemas."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Base schema with common configuration."""
    
    model_config = ConfigDict(from_attributes=True)


class BaseResponse(BaseSchema):
    """Base response schema with common fields."""
    
    id: int
    created_at: datetime
    updated_at: datetime


class MessageResponse(BaseSchema):
    """Simple message response."""
    
    message: str


class TokenResponse(BaseSchema):
    """Token response."""
    
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
