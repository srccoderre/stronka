"""Finance service."""
from typing import List, Optional
from datetime import date, datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError, AuthorizationError
from app.core.config import settings
from app.models.finance import DailyEntry, Investment, MonthlyGoal
from app.repositories.finance import (
    daily_entry_repository,
    investment_repository,
    monthly_goal_repository,
)
from app.schemas.finance import (
    DailyEntryCreate,
    DailyEntryUpdate,
    InvestmentCreate,
    InvestmentUpdate,
    MonthlyGoalCreate,
    MonthlyGoalUpdate,
    InvestmentSummary,
)


class FinanceService:
    """Finance service."""
    
    # Daily Entries
    async def create_entry(
        self,
        db: AsyncSession,
        user_id: int,
        entry_create: DailyEntryCreate,
    ) -> DailyEntry:
        """Create daily entry."""
        entry_data = entry_create.model_dump()
        entry_data["user_id"] = user_id
        return await daily_entry_repository.create(db, entry_data)
    
    async def get_entry(
        self,
        db: AsyncSession,
        entry_id: int,
        user_id: int,
    ) -> DailyEntry:
        """Get daily entry by ID."""
        entry = await daily_entry_repository.get(db, entry_id)
        if not entry:
            raise NotFoundError("Entry not found")
        if entry.user_id != user_id:
            raise AuthorizationError("Not authorized to access this entry")
        return entry
    
    async def get_entries(
        self,
        db: AsyncSession,
        user_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[DailyEntry]:
        """Get user's daily entries."""
        if start_date and end_date:
            return await daily_entry_repository.get_by_date_range(
                db, user_id, start_date, end_date
            )
        return await daily_entry_repository.get_multi(
            db, skip=skip, limit=limit, filters={"user_id": user_id}
        )
    
    async def update_entry(
        self,
        db: AsyncSession,
        entry_id: int,
        user_id: int,
        entry_update: DailyEntryUpdate,
    ) -> DailyEntry:
        """Update daily entry."""
        entry = await self.get_entry(db, entry_id, user_id)
        update_data = entry_update.model_dump(exclude_unset=True)
        return await daily_entry_repository.update(db, entry, update_data)
    
    async def delete_entry(
        self,
        db: AsyncSession,
        entry_id: int,
        user_id: int,
    ) -> bool:
        """Delete daily entry."""
        entry = await self.get_entry(db, entry_id, user_id)
        return await daily_entry_repository.delete(db, entry_id)
    
    # Investments
    async def create_investment(
        self,
        db: AsyncSession,
        user_id: int,
        investment_create: InvestmentCreate,
    ) -> Investment:
        """Create investment."""
        investment_data = investment_create.model_dump()
        investment_data["user_id"] = user_id
        return await investment_repository.create(db, investment_data)
    
    async def get_investment(
        self,
        db: AsyncSession,
        investment_id: int,
        user_id: int,
    ) -> Investment:
        """Get investment by ID."""
        investment = await investment_repository.get(db, investment_id)
        if not investment:
            raise NotFoundError("Investment not found")
        if investment.user_id != user_id:
            raise AuthorizationError("Not authorized to access this investment")
        return investment
    
    async def get_investments(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> List[Investment]:
        """Get user's investments."""
        return await investment_repository.get_by_user(db, user_id)
    
    async def get_investment_summary(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> List[InvestmentSummary]:
        """Get investment summary by type."""
        summary_data = await investment_repository.get_summary_by_type(db, user_id)
        return [InvestmentSummary(**item) for item in summary_data]
    
    async def update_investment(
        self,
        db: AsyncSession,
        investment_id: int,
        user_id: int,
        investment_update: InvestmentUpdate,
    ) -> Investment:
        """Update investment."""
        investment = await self.get_investment(db, investment_id, user_id)
        update_data = investment_update.model_dump(exclude_unset=True)
        return await investment_repository.update(db, investment, update_data)
    
    async def delete_investment(
        self,
        db: AsyncSession,
        investment_id: int,
        user_id: int,
    ) -> bool:
        """Delete investment."""
        investment = await self.get_investment(db, investment_id, user_id)
        return await investment_repository.delete(db, investment_id)
    
    # Monthly Goals
    async def get_or_create_monthly_goal(
        self,
        db: AsyncSession,
        user_id: int,
        year: int,
        month: int,
    ) -> MonthlyGoal:
        """Get or create monthly goal with defaults."""
        goal = await monthly_goal_repository.get_by_month(db, user_id, year, month)
        
        if not goal:
            # Create with default values
            goal_data = {
                "user_id": user_id,
                "year": year,
                "month": month,
                "income_goal": settings.DEFAULT_MONTHLY_INCOME_GOAL,
                "gold_goal": settings.DEFAULT_MONTHLY_GOLD_GOAL,
                "silver_goal": settings.DEFAULT_MONTHLY_SILVER_GOAL,
                "investment_goal": settings.DEFAULT_MONTHLY_INVESTMENT_GOAL,
            }
            goal = await monthly_goal_repository.create(db, goal_data)
        
        return goal
    
    async def update_monthly_goal(
        self,
        db: AsyncSession,
        user_id: int,
        year: int,
        month: int,
        goal_update: MonthlyGoalUpdate,
    ) -> MonthlyGoal:
        """Update monthly goal."""
        goal = await self.get_or_create_monthly_goal(db, user_id, year, month)
        update_data = goal_update.model_dump(exclude_unset=True)
        return await monthly_goal_repository.update(db, goal, update_data)
    
    async def get_yearly_goals(
        self,
        db: AsyncSession,
        user_id: int,
        year: int,
    ) -> List[MonthlyGoal]:
        """Get all goals for a year."""
        return await monthly_goal_repository.get_by_year(db, user_id, year)


finance_service = FinanceService()
