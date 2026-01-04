"""Repositories initialization."""
from app.repositories.base import BaseRepository
from app.repositories.user import UserRepository, user_repository
from app.repositories.finance import (
    DailyEntryRepository,
    InvestmentRepository,
    MonthlyGoalRepository,
    daily_entry_repository,
    investment_repository,
    monthly_goal_repository,
)

__all__ = [
    "BaseRepository",
    "UserRepository",
    "user_repository",
    "DailyEntryRepository",
    "InvestmentRepository",
    "MonthlyGoalRepository",
    "daily_entry_repository",
    "investment_repository",
    "monthly_goal_repository",
]
