"""Daily entries endpoints."""
from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.exceptions import NotFoundError, AuthorizationError
from app.schemas.finance import DailyEntryCreate, DailyEntryUpdate, DailyEntryResponse
from app.schemas.base import MessageResponse
from app.services.finance import finance_service
from app.api.v1.deps import get_current_active_user
from app.models.user import User

router = APIRouter()


@router.get("", response_model=List[DailyEntryResponse])
async def get_daily_entries(
    start_date: Optional[date] = Query(None, description="Start date for filtering"),
    end_date: Optional[date] = Query(None, description="End date for filtering"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> List:
    """
    Get daily entries for current user.
    
    Args:
        start_date: Optional start date filter
        end_date: Optional end date filter
        skip: Number of records to skip
        limit: Maximum number of records
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        List of daily entries
    """
    entries = await finance_service.get_entries(
        db, current_user.id, start_date, end_date, skip, limit
    )
    return entries


@router.post("", response_model=DailyEntryResponse, status_code=status.HTTP_201_CREATED)
async def create_daily_entry(
    entry_create: DailyEntryCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> DailyEntryResponse:
    """
    Create a new daily entry.
    
    Args:
        entry_create: Entry creation data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Created entry
    """
    entry = await finance_service.create_entry(db, current_user.id, entry_create)
    return entry


@router.get("/{entry_id}", response_model=DailyEntryResponse)
async def get_daily_entry(
    entry_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> DailyEntryResponse:
    """
    Get a specific daily entry.
    
    Args:
        entry_id: Entry ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Daily entry
    """
    try:
        entry = await finance_service.get_entry(db, entry_id, current_user.id)
        return entry
    except (NotFoundError, AuthorizationError) as e:
        status_code = status.HTTP_404_NOT_FOUND if isinstance(e, NotFoundError) else status.HTTP_403_FORBIDDEN
        raise HTTPException(status_code=status_code, detail=str(e))


@router.patch("/{entry_id}", response_model=DailyEntryResponse)
async def update_daily_entry(
    entry_id: int,
    entry_update: DailyEntryUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> DailyEntryResponse:
    """
    Update a daily entry.
    
    Args:
        entry_id: Entry ID
        entry_update: Entry update data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Updated entry
    """
    try:
        entry = await finance_service.update_entry(db, entry_id, current_user.id, entry_update)
        return entry
    except (NotFoundError, AuthorizationError) as e:
        status_code = status.HTTP_404_NOT_FOUND if isinstance(e, NotFoundError) else status.HTTP_403_FORBIDDEN
        raise HTTPException(status_code=status_code, detail=str(e))


@router.delete("/{entry_id}", response_model=MessageResponse)
async def delete_daily_entry(
    entry_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> MessageResponse:
    """
    Delete a daily entry.
    
    Args:
        entry_id: Entry ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Success message
    """
    try:
        await finance_service.delete_entry(db, entry_id, current_user.id)
        return MessageResponse(message="Entry deleted successfully")
    except (NotFoundError, AuthorizationError) as e:
        status_code = status.HTTP_404_NOT_FOUND if isinstance(e, NotFoundError) else status.HTTP_403_FORBIDDEN
        raise HTTPException(status_code=status_code, detail=str(e))
