"""User model."""
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class User(BaseModel):
    """User model."""
    
    __tablename__ = "users"
    
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    daily_entries = relationship("DailyEntry", back_populates="user", cascade="all, delete-orphan")
    investments = relationship("Investment", back_populates="user", cascade="all, delete-orphan")
    monthly_goals = relationship("MonthlyGoal", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<User {self.username}>"
