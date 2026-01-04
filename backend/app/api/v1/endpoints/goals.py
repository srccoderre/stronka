"""Goals endpoints."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.finance import MonthlyGoalResponse, MonthlyGoalUpdate
from app.services.finance import finance_service
from app.api.v1.deps import get_current_active_user
from app.models.user import User

router = APIRouter()


@router.get("/monthly/{year}/{month}", response_model=MonthlyGoalResponse)
async def get_monthly_goal(
    year: int,
    month: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> MonthlyGoalResponse:
    """
    Get monthly goal (creates with defaults if not exists).
    
    Args:
        year: Year
        month: Month (1-12)
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Monthly goal
    """
    if month < 1 or month > 12:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Month must be between 1 and 12"
        )
    
    goal = await finance_service.get_or_create_monthly_goal(
        db, current_user.id, year, month
    )
    return goal


@router.put("/monthly/{year}/{month}", response_model=MonthlyGoalResponse)
async def update_monthly_goal(
    year: int,
    month: int,
    goal_update: MonthlyGoalUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> MonthlyGoalResponse:
    """
    Update monthly goal.
    
    Args:
        year: Year
        month: Month (1-12)
        goal_update: Goal update data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Updated goal
    """
    if month < 1 or month > 12:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Month must be between 1 and 12"
        )
    
    goal = await finance_service.update_monthly_goal(
        db, current_user.id, year, month, goal_update
    )
    return goal


@router.get("/yearly/{year}", response_model=List[MonthlyGoalResponse])
async def get_yearly_goals(
    year: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> List[MonthlyGoalResponse]:
    """
    Get all goals for a year.
    
    Args:
        year: Year
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        List of monthly goals
    """
    goals = await finance_service.get_yearly_goals(db, current_user.id, year)
    return goals
