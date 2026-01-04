"""Notification model."""
from sqlalchemy import Column, String, Integer, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Notification(BaseModel):
    """Notification model."""
    
    __tablename__ = "notifications"
    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), nullable=False)  # info, warning, success, error
    is_read = Column(Boolean, default=False, nullable=False, index=True)
    
    # Relationship
    user = relationship("User", back_populates="notifications")
    
    def __repr__(self) -> str:
        return f"<Notification {self.title} - User {self.user_id}>"
