"""Analytics service."""
from typing import List, Dict, Any
from datetime import date, datetime
from sqlalchemy.ext.asyncio import AsyncSession
from collections import defaultdict

from app.repositories.finance import (
    daily_entry_repository,
    investment_repository,
    monthly_goal_repository,
)
from app.schemas.finance import (
    DashboardStats,
    MonthlyAnalytics,
    AnnualAnalytics,
    CategoryBreakdown,
    MonthlyGoalResponse,
)
from app.models.finance import ExpenseCategory


class AnalyticsService:
    """Analytics service."""
    
    async def get_dashboard_stats(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> DashboardStats:
        """Get dashboard statistics."""
        now = datetime.now()
        current_year = now.year
        current_month = now.month
        
        # Get current month entries
        entries = await daily_entry_repository.get_by_month(
            db, user_id, current_year, current_month
        )
        
        # Calculate current month totals
        current_month_income = sum(e.income for e in entries)
        current_month_expense = sum(e.expense for e in entries)
        current_month_net = current_month_income - current_month_expense
        total_gold = sum(e.gold_grams for e in entries)
        total_silver = sum(e.silver_grams for e in entries)
        
        # Get investments value
        investments = await investment_repository.get_by_user(db, user_id)
        total_investments_value = sum(
            inv.current_value or inv.amount for inv in investments
        )
        
        # Get monthly goal
        goal = await monthly_goal_repository.get_by_month(
            db, user_id, current_year, current_month
        )
        
        monthly_goal_progress = None
        if goal:
            monthly_goal_progress = {
                "income_progress": (current_month_income / goal.income_goal * 100) if goal.income_goal else 0,
                "gold_progress": (total_gold / goal.gold_goal * 100) if goal.gold_goal else 0,
                "silver_progress": (total_silver / goal.silver_goal * 100) if goal.silver_goal else 0,
            }
        
        return DashboardStats(
            current_month_income=current_month_income,
            current_month_expense=current_month_expense,
            current_month_net=current_month_net,
            total_investments_value=total_investments_value,
            total_gold=total_gold,
            total_silver=total_silver,
            monthly_goal_progress=monthly_goal_progress,
            recent_entries_count=len(entries),
        )
    
    async def get_monthly_analytics(
        self,
        db: AsyncSession,
        user_id: int,
        year: int,
        month: int,
    ) -> MonthlyAnalytics:
        """Get monthly analytics."""
        entries = await daily_entry_repository.get_by_month(db, user_id, year, month)
        
        # Calculate totals
        total_income = sum(e.income for e in entries)
        total_expense = sum(e.expense for e in entries)
        net_income = total_income - total_expense
        total_gold = sum(e.gold_grams for e in entries)
        total_silver = sum(e.silver_grams for e in entries)
        
        # Category breakdown
        category_totals: Dict[str, float] = defaultdict(float)
        for entry in entries:
            if entry.expense > 0 and entry.expense_category:
                category_totals[entry.expense_category.value] += entry.expense
        
        category_breakdown = []
        for category, amount in category_totals.items():
            percentage = (amount / total_expense * 100) if total_expense > 0 else 0
            category_breakdown.append(
                CategoryBreakdown(
                    category=category,
                    amount=amount,
                    percentage=percentage
                )
            )
        
        # Get goal
        goal = await monthly_goal_repository.get_by_month(db, user_id, year, month)
        goal_response = MonthlyGoalResponse.model_validate(goal) if goal else None
        
        return MonthlyAnalytics(
            year=year,
            month=month,
            total_income=total_income,
            total_expense=total_expense,
            net_income=net_income,
            total_gold=total_gold,
            total_silver=total_silver,
            category_breakdown=category_breakdown,
            goal_progress=goal_response,
        )
    
    async def get_annual_analytics(
        self,
        db: AsyncSession,
        user_id: int,
        year: int,
    ) -> AnnualAnalytics:
        """Get annual analytics."""
        # Get monthly analytics for each month
        monthly_data = []
        total_income = 0.0
        total_expense = 0.0
        total_gold = 0.0
        total_silver = 0.0
        
        for month in range(1, 13):
            monthly = await self.get_monthly_analytics(db, user_id, year, month)
            monthly_data.append(monthly)
            total_income += monthly.total_income
            total_expense += monthly.total_expense
            total_gold += monthly.total_gold
            total_silver += monthly.total_silver
        
        # Get total investments
        investments = await investment_repository.get_by_user(db, user_id)
        total_investments = sum(
            inv.current_value or inv.amount for inv in investments
        )
        
        return AnnualAnalytics(
            year=year,
            total_income=total_income,
            total_expense=total_expense,
            net_income=total_income - total_expense,
            total_gold=total_gold,
            total_silver=total_silver,
            total_investments=total_investments,
            monthly_breakdown=monthly_data,
        )


analytics_service = AnalyticsService()
