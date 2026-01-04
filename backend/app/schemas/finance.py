"""Finance schemas."""
from typing import Optional, List
from datetime import date
from pydantic import Field
from app.schemas.base import BaseSchema, BaseResponse
from app.models.finance import ExpenseCategory, InvestmentType


# Daily Entry Schemas
class DailyEntryBase(BaseSchema):
    """Base daily entry schema."""
    
    date: date
    income: float = Field(default=0.0, ge=0)
    income_description: Optional[str] = None
    expense: float = Field(default=0.0, ge=0)
    expense_category: Optional[ExpenseCategory] = None
    expense_description: Optional[str] = None
    gold_grams: float = Field(default=0.0, ge=0)
    silver_grams: float = Field(default=0.0, ge=0)
    notes: Optional[str] = None


class DailyEntryCreate(DailyEntryBase):
    """Schema for creating daily entry."""
    pass


class DailyEntryUpdate(BaseSchema):
    """Schema for updating daily entry."""
    
    income: Optional[float] = Field(None, ge=0)
    income_description: Optional[str] = None
    expense: Optional[float] = Field(None, ge=0)
    expense_category: Optional[ExpenseCategory] = None
    expense_description: Optional[str] = None
    gold_grams: Optional[float] = Field(None, ge=0)
    silver_grams: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = None


class DailyEntryResponse(BaseResponse, DailyEntryBase):
    """Daily entry response schema."""
    
    user_id: int


# Investment Schemas
class InvestmentBase(BaseSchema):
    """Base investment schema."""
    
    investment_type: InvestmentType
    name: str = Field(..., max_length=255)
    amount: float = Field(..., gt=0)
    quantity: Optional[float] = Field(None, gt=0)
    purchase_date: date
    current_value: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = None


class InvestmentCreate(InvestmentBase):
    """Schema for creating investment."""
    pass


class InvestmentUpdate(BaseSchema):
    """Schema for updating investment."""
    
    name: Optional[str] = Field(None, max_length=255)
    amount: Optional[float] = Field(None, gt=0)
    quantity: Optional[float] = Field(None, gt=0)
    current_value: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = None


class InvestmentResponse(BaseResponse, InvestmentBase):
    """Investment response schema."""
    
    user_id: int


class InvestmentSummary(BaseSchema):
    """Investment summary by type."""
    
    investment_type: InvestmentType
    total_amount: float
    total_current_value: float
    count: int


# Monthly Goal Schemas
class MonthlyGoalBase(BaseSchema):
    """Base monthly goal schema."""
    
    income_goal: float = Field(..., ge=0)
    gold_goal: float = Field(..., ge=0)
    silver_goal: float = Field(..., ge=0)
    investment_goal: float = Field(..., ge=0)


class MonthlyGoalCreate(MonthlyGoalBase):
    """Schema for creating monthly goal."""
    
    year: int = Field(..., ge=2000, le=2100)
    month: int = Field(..., ge=1, le=12)


class MonthlyGoalUpdate(BaseSchema):
    """Schema for updating monthly goal."""
    
    income_goal: Optional[float] = Field(None, ge=0)
    gold_goal: Optional[float] = Field(None, ge=0)
    silver_goal: Optional[float] = Field(None, ge=0)
    investment_goal: Optional[float] = Field(None, ge=0)


class MonthlyGoalResponse(BaseResponse, MonthlyGoalBase):
    """Monthly goal response schema."""
    
    user_id: int
    year: int
    month: int


# Analytics Schemas
class CategoryBreakdown(BaseSchema):
    """Category breakdown."""
    
    category: str
    amount: float
    percentage: float


class MonthlyAnalytics(BaseSchema):
    """Monthly analytics."""
    
    year: int
    month: int
    total_income: float
    total_expense: float
    net_income: float
    total_gold: float
    total_silver: float
    category_breakdown: List[CategoryBreakdown]
    goal_progress: Optional[MonthlyGoalResponse] = None


class AnnualAnalytics(BaseSchema):
    """Annual analytics."""
    
    year: int
    total_income: float
    total_expense: float
    net_income: float
    total_gold: float
    total_silver: float
    total_investments: float
    monthly_breakdown: List[MonthlyAnalytics]


class DashboardStats(BaseSchema):
    """Dashboard statistics."""
    
    current_month_income: float
    current_month_expense: float
    current_month_net: float
    total_investments_value: float
    total_gold: float
    total_silver: float
    monthly_goal_progress: Optional[dict] = None
    recent_entries_count: int
