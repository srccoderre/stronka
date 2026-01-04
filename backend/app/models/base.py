"""Base model with common fields."""
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Boolean
from app.core.database import Base


class BaseModel(Base):
    """Base model with common fields for all models."""
    
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)
