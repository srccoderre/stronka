"""User service."""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_password_hash, verify_password
from app.core.exceptions import AuthenticationError, NotFoundError, ValidationError
from app.models.user import User
from app.repositories.user import user_repository
from app.schemas.user import UserUpdate, ChangePassword


class UserService:
    """User service."""
    
    async def get_user(self, db: AsyncSession, user_id: int) -> User:
        """Get user by ID."""
        user = await user_repository.get(db, user_id)
        if not user:
            raise NotFoundError("User not found")
        return user
    
    async def update_profile(
        self,
        db: AsyncSession,
        user_id: int,
        user_update: UserUpdate,
    ) -> User:
        """Update user profile."""
        user = await self.get_user(db, user_id)
        
        # Check if email is being changed and if it's already taken
        if user_update.email and user_update.email != user.email:
            existing = await user_repository.get_by_email(db, user_update.email)
            if existing:
                raise ValidationError("Email already in use")
        
        update_data = user_update.model_dump(exclude_unset=True)
        updated_user = await user_repository.update(db, user, update_data)
        
        return updated_user
    
    async def change_password(
        self,
        db: AsyncSession,
        user_id: int,
        password_data: ChangePassword,
    ) -> User:
        """Change user password."""
        user = await self.get_user(db, user_id)
        
        # Verify current password
        if not verify_password(password_data.current_password, user.hashed_password):
            raise AuthenticationError("Current password is incorrect")
        
        # Update password
        user.hashed_password = get_password_hash(password_data.new_password)
        await db.flush()
        
        return user
    
    async def delete_account(self, db: AsyncSession, user_id: int) -> bool:
        """Soft delete user account."""
        return await user_repository.delete(db, user_id, soft=True)


user_service = UserService()
