"""User repository."""
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """User repository."""
    
    def __init__(self):
        super().__init__(User)
    
    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        """
        Get user by email.
        
        Args:
            db: Database session
            email: User email
            
        Returns:
            User instance or None
        """
        stmt = select(User).where(
            User.email == email,
            User.is_deleted == False
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_username(self, db: AsyncSession, username: str) -> Optional[User]:
        """
        Get user by username.
        
        Args:
            db: Database session
            username: Username
            
        Returns:
            User instance or None
        """
        stmt = select(User).where(
            User.username == username,
            User.is_deleted == False
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def authenticate(
        self,
        db: AsyncSession,
        username: str,
        password: str,
    ) -> Optional[User]:
        """
        Authenticate user.
        
        Args:
            db: Database session
            username: Username
            password: Plain password
            
        Returns:
            User instance if authenticated, None otherwise
        """
        from app.core.security import verify_password
        
        user = await self.get_by_username(db, username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user


user_repository = UserRepository()
