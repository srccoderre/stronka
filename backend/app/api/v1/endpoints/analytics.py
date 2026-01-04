"""Analytics endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.finance import DashboardStats, MonthlyAnalytics, AnnualAnalytics
from app.services.analytics import analytics_service
from app.api.v1.deps import get_current_active_user
from app.models.user import User

router = APIRouter()


@router.get("/dashboard", response_model=DashboardStats)
async def get_dashboard_stats(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> DashboardStats:
    """
    Get dashboard statistics.
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Dashboard statistics
    """
    stats = await analytics_service.get_dashboard_stats(db, current_user.id)
    return stats


@router.get("/monthly/{year}/{month}", response_model=MonthlyAnalytics)
async def get_monthly_analytics(
    year: int,
    month: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> MonthlyAnalytics:
    """
    Get monthly analytics.
    
    Args:
        year: Year
        month: Month (1-12)
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Monthly analytics
    """
    if month < 1 or month > 12:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Month must be between 1 and 12"
        )
    
    analytics = await analytics_service.get_monthly_analytics(
        db, current_user.id, year, month
    )
    return analytics


@router.get("/annual/{year}", response_model=AnnualAnalytics)
async def get_annual_analytics(
    year: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> AnnualAnalytics:
    """
    Get annual analytics.
    
    Args:
        year: Year
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Annual analytics
    """
    analytics = await analytics_service.get_annual_analytics(db, current_user.id, year)
    return analytics
