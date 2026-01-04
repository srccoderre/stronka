"""API dependencies."""
from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.exceptions import AuthenticationError
from app.models.user import User
from app.services.auth import auth_service

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Get current authenticated user.
    
    Args:
        credentials: HTTP authorization credentials
        db: Database session
        
    Returns:
        Current user
        
    Raises:
        HTTPException: If authentication fails
    """
    try:
        token = credentials.credentials
        user = await auth_service.get_current_user(db, token)
        return user
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Get current active user.
    
    Args:
        current_user: Current user from token
        
    Returns:
        Current active user
        
    Raises:
        HTTPException: If user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user


async def get_current_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Get current superuser.
    
    Args:
        current_user: Current user from token
        
    Returns:
        Current superuser
        
    Raises:
        HTTPException: If user is not a superuser
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user
