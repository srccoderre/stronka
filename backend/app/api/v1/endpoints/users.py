"""User endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.exceptions import NotFoundError, ValidationError, AuthenticationError
from app.schemas.user import UserResponse, UserUpdate, ChangePassword
from app.schemas.base import MessageResponse
from app.services.user import user_service
from app.api.v1.deps import get_current_active_user
from app.models.user import User

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Get current user profile.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User profile
    """
    return current_user


@router.patch("/me", response_model=UserResponse)
async def update_current_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Update current user profile.
    
    Args:
        user_update: User update data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Updated user
    """
    try:
        user = await user_service.update_profile(db, current_user.id, user_update)
        return user
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )


@router.post("/me/change-password", response_model=MessageResponse)
async def change_password(
    password_data: ChangePassword,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> MessageResponse:
    """
    Change user password.
    
    Args:
        password_data: Password change data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Success message
    """
    try:
        await user_service.change_password(db, current_user.id, password_data)
        return MessageResponse(message="Password changed successfully")
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@router.delete("/me", response_model=MessageResponse)
async def delete_current_user(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> MessageResponse:
    """
    Delete current user account (soft delete).
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Success message
    """
    await user_service.delete_account(db, current_user.id)
    return MessageResponse(message="Account deleted successfully")
