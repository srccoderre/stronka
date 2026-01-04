"""Finance repositories."""
from typing import List, Optional
from datetime import date
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.finance import DailyEntry, Investment, MonthlyGoal, InvestmentType
from app.repositories.base import BaseRepository


class DailyEntryRepository(BaseRepository[DailyEntry]):
    """Daily entry repository."""
    
    def __init__(self):
        super().__init__(DailyEntry)
    
    async def get_by_date_range(
        self,
        db: AsyncSession,
        user_id: int,
        start_date: date,
        end_date: date,
    ) -> List[DailyEntry]:
        """Get entries within date range for user."""
        stmt = select(DailyEntry).where(
            and_(
                DailyEntry.user_id == user_id,
                DailyEntry.date >= start_date,
                DailyEntry.date <= end_date,
                DailyEntry.is_deleted == False
            )
        ).order_by(DailyEntry.date.desc())
        
        result = await db.execute(stmt)
        return list(result.scalars().all())
    
    async def get_by_month(
        self,
        db: AsyncSession,
        user_id: int,
        year: int,
        month: int,
    ) -> List[DailyEntry]:
        """Get entries for specific month."""
        stmt = select(DailyEntry).where(
            and_(
                DailyEntry.user_id == user_id,
                func.extract('year', DailyEntry.date) == year,
                func.extract('month', DailyEntry.date) == month,
                DailyEntry.is_deleted == False
            )
        ).order_by(DailyEntry.date.desc())
        
        result = await db.execute(stmt)
        return list(result.scalars().all())


class InvestmentRepository(BaseRepository[Investment]):
    """Investment repository."""
    
    def __init__(self):
        super().__init__(Investment)
    
    async def get_by_user(
        self,
        db: AsyncSession,
        user_id: int,
        investment_type: Optional[InvestmentType] = None,
    ) -> List[Investment]:
        """Get investments for user, optionally filtered by type."""
        stmt = select(Investment).where(
            and_(
                Investment.user_id == user_id,
                Investment.is_deleted == False
            )
        )
        
        if investment_type:
            stmt = stmt.where(Investment.investment_type == investment_type)
        
        stmt = stmt.order_by(Investment.purchase_date.desc())
        result = await db.execute(stmt)
        return list(result.scalars().all())
    
    async def get_summary_by_type(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> List[dict]:
        """Get investment summary grouped by type."""
        stmt = select(
            Investment.investment_type,
            func.sum(Investment.amount).label('total_amount'),
            func.sum(Investment.current_value).label('total_current_value'),
            func.count(Investment.id).label('count')
        ).where(
            and_(
                Investment.user_id == user_id,
                Investment.is_deleted == False
            )
        ).group_by(Investment.investment_type)
        
        result = await db.execute(stmt)
        return [
            {
                "investment_type": row[0],
                "total_amount": float(row[1] or 0),
                "total_current_value": float(row[2] or 0),
                "count": row[3]
            }
            for row in result
        ]


class MonthlyGoalRepository(BaseRepository[MonthlyGoal]):
    """Monthly goal repository."""
    
    def __init__(self):
        super().__init__(MonthlyGoal)
    
    async def get_by_month(
        self,
        db: AsyncSession,
        user_id: int,
        year: int,
        month: int,
    ) -> Optional[MonthlyGoal]:
        """Get goal for specific month."""
        stmt = select(MonthlyGoal).where(
            and_(
                MonthlyGoal.user_id == user_id,
                MonthlyGoal.year == year,
                MonthlyGoal.month == month,
                MonthlyGoal.is_deleted == False
            )
        )
        
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_year(
        self,
        db: AsyncSession,
        user_id: int,
        year: int,
    ) -> List[MonthlyGoal]:
        """Get all goals for a year."""
        stmt = select(MonthlyGoal).where(
            and_(
                MonthlyGoal.user_id == user_id,
                MonthlyGoal.year == year,
                MonthlyGoal.is_deleted == False
            )
        ).order_by(MonthlyGoal.month)
        
        result = await db.execute(stmt)
        return list(result.scalars().all())


# Repository instances
daily_entry_repository = DailyEntryRepository()
investment_repository = InvestmentRepository()
monthly_goal_repository = MonthlyGoalRepository()
