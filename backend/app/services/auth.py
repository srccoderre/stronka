"""Authentication service."""
from datetime import datetime, timedelta
from typing import Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.core.exceptions import AuthenticationError, ConflictError, NotFoundError
from app.models.user import User
from app.repositories.user import user_repository
from app.schemas.user import UserCreate, UserLogin
from app.schemas.base import TokenResponse


class AuthService:
    """Authentication service."""
    
    async def register(
        self,
        db: AsyncSession,
        user_create: UserCreate,
    ) -> User:
        """
        Register a new user.
        
        Args:
            db: Database session
            user_create: User creation data
            
        Returns:
            Created user
            
        Raises:
            ConflictError: If email or username already exists
        """
        # Check if email exists
        existing_user = await user_repository.get_by_email(db, user_create.email)
        if existing_user:
            raise ConflictError("Email already registered")
        
        # Check if username exists
        existing_user = await user_repository.get_by_username(db, user_create.username)
        if existing_user:
            raise ConflictError("Username already taken")
        
        # Create user
        user_data = user_create.model_dump(exclude={"password"})
        user_data["hashed_password"] = get_password_hash(user_create.password)
        
        user = await user_repository.create(db, user_data)
        return user
    
    async def login(
        self,
        db: AsyncSession,
        user_login: UserLogin,
    ) -> Tuple[User, TokenResponse]:
        """
        Authenticate user and generate tokens.
        
        Args:
            db: Database session
            user_login: Login credentials
            
        Returns:
            Tuple of (User, TokenResponse)
            
        Raises:
            AuthenticationError: If credentials are invalid
        """
        user = await user_repository.authenticate(
            db,
            user_login.username,
            user_login.password
        )
        
        if not user:
            raise AuthenticationError("Invalid username or password")
        
        if not user.is_active:
            raise AuthenticationError("User account is inactive")
        
        # Update last login
        user.last_login = datetime.utcnow()
        await db.flush()
        
        # Generate tokens
        token_data = {"sub": str(user.id), "username": user.username}
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)
        
        tokens = TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )
        
        return user, tokens
    
    async def refresh_token(
        self,
        db: AsyncSession,
        refresh_token: str,
    ) -> TokenResponse:
        """
        Refresh access token.
        
        Args:
            db: Database session
            refresh_token: Refresh token
            
        Returns:
            New token pair
            
        Raises:
            AuthenticationError: If token is invalid
        """
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise AuthenticationError("Invalid refresh token")
        
        user_id = int(payload.get("sub"))
        user = await user_repository.get(db, user_id)
        
        if not user or not user.is_active:
            raise AuthenticationError("User not found or inactive")
        
        # Generate new tokens
        token_data = {"sub": str(user.id), "username": user.username}
        access_token = create_access_token(token_data)
        new_refresh_token = create_refresh_token(token_data)
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
        )
    
    async def get_current_user(
        self,
        db: AsyncSession,
        token: str,
    ) -> User:
        """
        Get current user from access token.
        
        Args:
            db: Database session
            token: Access token
            
        Returns:
            Current user
            
        Raises:
            AuthenticationError: If token is invalid
        """
        payload = decode_token(token)
        if not payload or payload.get("type") != "access":
            raise AuthenticationError("Invalid access token")
        
        user_id = int(payload.get("sub"))
        user = await user_repository.get(db, user_id)
        
        if not user or not user.is_active:
            raise AuthenticationError("User not found or inactive")
        
        return user


auth_service = AuthService()
