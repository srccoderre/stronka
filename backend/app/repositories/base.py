"""Base repository with common CRUD operations."""
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    """Base repository with common CRUD operations."""
    
    def __init__(self, model: Type[ModelType]):
        """
        Initialize repository.
        
        Args:
            model: SQLAlchemy model class
        """
        self.model = model
    
    async def get(self, db: AsyncSession, id: int, include_deleted: bool = False) -> Optional[ModelType]:
        """
        Get a single record by ID.
        
        Args:
            db: Database session
            id: Record ID
            include_deleted: Include soft-deleted records
            
        Returns:
            Model instance or None
        """
        stmt = select(self.model).where(self.model.id == id)
        if not include_deleted:
            stmt = stmt.where(self.model.is_deleted == False)
        
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_multi(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        include_deleted: bool = False,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[ModelType]:
        """
        Get multiple records with pagination.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            include_deleted: Include soft-deleted records
            filters: Additional filters as dict
            
        Returns:
            List of model instances
        """
        stmt = select(self.model)
        
        if not include_deleted:
            stmt = stmt.where(self.model.is_deleted == False)
        
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key):
                    stmt = stmt.where(getattr(self.model, key) == value)
        
        stmt = stmt.offset(skip).limit(limit)
        result = await db.execute(stmt)
        return list(result.scalars().all())
    
    async def create(self, db: AsyncSession, obj_in: Dict[str, Any]) -> ModelType:
        """
        Create a new record.
        
        Args:
            db: Database session
            obj_in: Data for creating record
            
        Returns:
            Created model instance
        """
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj
    
    async def update(
        self,
        db: AsyncSession,
        db_obj: ModelType,
        obj_in: Dict[str, Any],
    ) -> ModelType:
        """
        Update a record.
        
        Args:
            db: Database session
            db_obj: Existing model instance
            obj_in: Update data
            
        Returns:
            Updated model instance
        """
        for field, value in obj_in.items():
            if value is not None and hasattr(db_obj, field):
                setattr(db_obj, field, value)
        
        await db.flush()
        await db.refresh(db_obj)
        return db_obj
    
    async def delete(self, db: AsyncSession, id: int, soft: bool = True) -> bool:
        """
        Delete a record (soft or hard).
        
        Args:
            db: Database session
            id: Record ID
            soft: Perform soft delete if True, hard delete otherwise
            
        Returns:
            True if deleted, False otherwise
        """
        db_obj = await self.get(db, id)
        if not db_obj:
            return False
        
        if soft:
            db_obj.is_deleted = True
            await db.flush()
        else:
            await db.delete(db_obj)
            await db.flush()
        
        return True
