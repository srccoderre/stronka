"""Auth endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.database import get_db
from app.core.exceptions import AuthenticationError, ConflictError
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.schemas.base import TokenResponse, MessageResponse
from app.services.auth import auth_service
from app.api.v1.deps import get_current_user
from app.models.user import User

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_create: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Register a new user.
    
    Args:
        user_create: User registration data
        db: Database session
        
    Returns:
        Created user
    """
    try:
        user = await auth_service.register(db, user_create)
        return user
    except ConflictError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.post("/login", response_model=TokenResponse)
async def login(
    user_login: UserLogin,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    """
    Login user and return tokens.
    
    Args:
        user_login: Login credentials
        db: Database session
        
    Returns:
        Access and refresh tokens
    """
    try:
        user, tokens = await auth_service.login(db, user_login)
        return tokens
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_token: str,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    """
    Refresh access token.
    
    Args:
        refresh_token: Refresh token
        db: Database session
        
    Returns:
        New token pair
    """
    try:
        tokens = await auth_service.refresh_token(db, refresh_token)
        return tokens
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Get current user information.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Current user
    """
    return current_user


@router.post("/logout", response_model=MessageResponse)
async def logout() -> MessageResponse:
    """
    Logout user (client should delete tokens).
    
    Returns:
        Success message
    """
    return MessageResponse(message="Successfully logged out")


@router.post("/password-reset/request", response_model=MessageResponse)
async def request_password_reset(
    email: str,
    db: AsyncSession = Depends(get_db),
) -> MessageResponse:
    """
    Request password reset (placeholder - implement email sending).
    
    Args:
        email: User email
        db: Database session
        
    Returns:
        Success message
    """
    # TODO: Implement password reset token generation and email sending
    return MessageResponse(message="Password reset email sent")


@router.post("/password-reset/confirm", response_model=MessageResponse)
async def confirm_password_reset(
    token: str,
    new_password: str,
    db: AsyncSession = Depends(get_db),
) -> MessageResponse:
    """
    Confirm password reset (placeholder).
    
    Args:
        token: Reset token
        new_password: New password
        db: Database session
        
    Returns:
        Success message
    """
    # TODO: Implement password reset confirmation
    return MessageResponse(message="Password reset successful")
