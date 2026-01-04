"""Notification service."""
from typing import List
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notification import Notification
from app.core.exceptions import NotFoundError, AuthorizationError


class NotificationService:
    """Notification service."""
    
    async def create_notification(
        self,
        db: AsyncSession,
        user_id: int,
        title: str,
        message: str,
        notification_type: str = "info",
    ) -> Notification:
        """Create a notification."""
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
        )
        db.add(notification)
        await db.flush()
        await db.refresh(notification)
        return notification
    
    async def get_notifications(
        self,
        db: AsyncSession,
        user_id: int,
        unread_only: bool = False,
        skip: int = 0,
        limit: int = 50,
    ) -> List[Notification]:
        """Get user notifications."""
        stmt = select(Notification).where(
            and_(
                Notification.user_id == user_id,
                Notification.is_deleted == False
            )
        )
        
        if unread_only:
            stmt = stmt.where(Notification.is_read == False)
        
        stmt = stmt.order_by(Notification.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return list(result.scalars().all())
    
    async def get_unread_count(self, db: AsyncSession, user_id: int) -> int:
        """Get count of unread notifications."""
        stmt = select(func.count(Notification.id)).where(
            and_(
                Notification.user_id == user_id,
                Notification.is_read == False,
                Notification.is_deleted == False
            )
        )
        result = await db.execute(stmt)
        return result.scalar() or 0
    
    async def mark_as_read(
        self,
        db: AsyncSession,
        notification_id: int,
        user_id: int,
    ) -> Notification:
        """Mark notification as read."""
        stmt = select(Notification).where(Notification.id == notification_id)
        result = await db.execute(stmt)
        notification = result.scalar_one_or_none()
        
        if not notification:
            raise NotFoundError("Notification not found")
        
        if notification.user_id != user_id:
            raise AuthorizationError("Not authorized to access this notification")
        
        notification.is_read = True
        await db.flush()
        await db.refresh(notification)
        return notification
    
    async def mark_all_as_read(self, db: AsyncSession, user_id: int) -> int:
        """Mark all notifications as read."""
        stmt = select(Notification).where(
            and_(
                Notification.user_id == user_id,
                Notification.is_read == False,
                Notification.is_deleted == False
            )
        )
        result = await db.execute(stmt)
        notifications = result.scalars().all()
        
        count = 0
        for notification in notifications:
            notification.is_read = True
            count += 1
        
        await db.flush()
        return count
    
    async def delete_notification(
        self,
        db: AsyncSession,
        notification_id: int,
        user_id: int,
    ) -> bool:
        """Delete notification."""
        stmt = select(Notification).where(Notification.id == notification_id)
        result = await db.execute(stmt)
        notification = result.scalar_one_or_none()
        
        if not notification:
            return False
        
        if notification.user_id != user_id:
            raise AuthorizationError("Not authorized to delete this notification")
        
        notification.is_deleted = True
        await db.flush()
        return True


notification_service = NotificationService()
