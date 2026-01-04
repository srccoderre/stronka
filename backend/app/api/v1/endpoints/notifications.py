"""Notification endpoints."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.database import get_db
from app.core.exceptions import NotFoundError, AuthorizationError
from app.schemas.base import MessageResponse, BaseResponse
from app.services.notification import notification_service
from app.api.v1.deps import get_current_active_user
from app.models.user import User
from app.models.notification import Notification

router = APIRouter()


class NotificationResponse(BaseResponse):
    """Notification response schema."""
    user_id: int
    title: str
    message: str
    notification_type: str
    is_read: bool


class UnreadCountResponse(BaseModel):
    """Unread count response."""
    count: int


@router.get("", response_model=List[NotificationResponse])
async def get_notifications(
    unread_only: bool = Query(False, description="Get only unread notifications"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> List[Notification]:
    """
    Get notifications for current user.
    
    Args:
        unread_only: Filter for unread notifications
        skip: Number of records to skip
        limit: Maximum number of records
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        List of notifications
    """
    notifications = await notification_service.get_notifications(
        db, current_user.id, unread_only, skip, limit
    )
    return notifications


@router.get("/unread/count", response_model=UnreadCountResponse)
async def get_unread_count(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> UnreadCountResponse:
    """
    Get count of unread notifications.
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Unread count
    """
    count = await notification_service.get_unread_count(db, current_user.id)
    return UnreadCountResponse(count=count)


@router.post("/{notification_id}/read", response_model=NotificationResponse)
async def mark_notification_as_read(
    notification_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Notification:
    """
    Mark notification as read.
    
    Args:
        notification_id: Notification ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Updated notification
    """
    try:
        notification = await notification_service.mark_as_read(
            db, notification_id, current_user.id
        )
        return notification
    except (NotFoundError, AuthorizationError) as e:
        status_code = status.HTTP_404_NOT_FOUND if isinstance(e, NotFoundError) else status.HTTP_403_FORBIDDEN
        raise HTTPException(status_code=status_code, detail=str(e))


@router.post("/read-all", response_model=MessageResponse)
async def mark_all_as_read(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> MessageResponse:
    """
    Mark all notifications as read.
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Success message with count
    """
    count = await notification_service.mark_all_as_read(db, current_user.id)
    return MessageResponse(message=f"Marked {count} notifications as read")


@router.delete("/{notification_id}", response_model=MessageResponse)
async def delete_notification(
    notification_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> MessageResponse:
    """
    Delete a notification.
    
    Args:
        notification_id: Notification ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Success message
    """
    try:
        deleted = await notification_service.delete_notification(
            db, notification_id, current_user.id
        )
        if deleted:
            return MessageResponse(message="Notification deleted successfully")
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found"
            )
    except AuthorizationError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
