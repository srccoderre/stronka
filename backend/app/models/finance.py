"""Finance related models."""
import enum
from sqlalchemy import Column, String, Integer, Float, Date, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class ExpenseCategory(str, enum.Enum):
    """Expense categories."""
    FOOD = "FOOD"
    TRANSPORT = "TRANSPORT"
    ENTERTAINMENT = "ENTERTAINMENT"
    HOUSING = "HOUSING"
    UTILITIES = "UTILITIES"
    HEALTHCARE = "HEALTHCARE"
    EDUCATION = "EDUCATION"
    SHOPPING = "SHOPPING"
    SUBSCRIPTIONS = "SUBSCRIPTIONS"
    OTHER = "OTHER"


class InvestmentType(str, enum.Enum):
    """Investment types."""
    GOLD = "GOLD"
    SILVER = "SILVER"
    STOCKS = "STOCKS"
    BONDS = "BONDS"
    CRYPTO = "CRYPTO"
    ETF = "ETF"
    REAL_ESTATE = "REAL_ESTATE"
    SAVINGS = "SAVINGS"
    OTHER = "OTHER"


class DailyEntry(BaseModel):
    """Daily financial entry model."""
    
    __tablename__ = "daily_entries"
    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    
    # Income
    income = Column(Float, default=0.0, nullable=False)
    income_description = Column(Text, nullable=True)
    
    # Expenses
    expense = Column(Float, default=0.0, nullable=False)
    expense_category = Column(Enum(ExpenseCategory), nullable=True)
    expense_description = Column(Text, nullable=True)
    
    # Precious metals
    gold_grams = Column(Float, default=0.0, nullable=False)
    silver_grams = Column(Float, default=0.0, nullable=False)
    
    # Notes
    notes = Column(Text, nullable=True)
    
    # Relationship
    user = relationship("User", back_populates="daily_entries")
    
    def __repr__(self) -> str:
        return f"<DailyEntry {self.date} - User {self.user_id}>"


class Investment(BaseModel):
    """Investment model."""
    
    __tablename__ = "investments"
    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    investment_type = Column(Enum(InvestmentType), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)  # Amount in PLN
    quantity = Column(Float, nullable=True)  # Quantity (shares, coins, etc.)
    purchase_date = Column(Date, nullable=False, index=True)
    current_value = Column(Float, nullable=True)  # Current value in PLN
    notes = Column(Text, nullable=True)
    
    # Relationship
    user = relationship("User", back_populates="investments")
    
    def __repr__(self) -> str:
        return f"<Investment {self.name} - {self.investment_type}>"


class MonthlyGoal(BaseModel):
    """Monthly financial goal model."""
    
    __tablename__ = "monthly_goals"
    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    year = Column(Integer, nullable=False, index=True)
    month = Column(Integer, nullable=False, index=True)  # 1-12
    
    # Goals
    income_goal = Column(Float, nullable=False)  # PLN
    gold_goal = Column(Float, nullable=False)  # grams
    silver_goal = Column(Float, nullable=False)  # grams
    investment_goal = Column(Float, nullable=False)  # PLN
    
    # Relationship
    user = relationship("User", back_populates="monthly_goals")
    
    def __repr__(self) -> str:
        return f"<MonthlyGoal {self.year}-{self.month:02d} - User {self.user_id}>"
