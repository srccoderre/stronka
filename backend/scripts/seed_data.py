#!/usr/bin/env python3
"""Seed database with sample data."""
import asyncio
from datetime import date, datetime, timedelta
import random

from app.core.database import AsyncSessionLocal
from app.core.security import get_password_hash
from app.models.user import User
from app.models.finance import DailyEntry, Investment, MonthlyGoal, ExpenseCategory, InvestmentType


async def seed_database():
    """Seed database with sample data."""
    print("=== Seeding Database ===\n")
    
    async with AsyncSessionLocal() as db:
        # Create demo user
        demo_user = User(
            email="demo@mojportfel.pl",
            username="demo",
            full_name="Demo User",
            hashed_password=get_password_hash("demo123"),
            is_active=True,
            is_superuser=False,
        )
        db.add(demo_user)
        await db.flush()
        print(f"✓ Created demo user (username: demo, password: demo123)")
        
        # Create daily entries for last 30 days
        categories = list(ExpenseCategory)
        for i in range(30):
            entry_date = date.today() - timedelta(days=i)
            entry = DailyEntry(
                user_id=demo_user.id,
                date=entry_date,
                income=random.uniform(0, 5000) if random.random() > 0.7 else 0,
                expense=random.uniform(50, 1000),
                expense_category=random.choice(categories),
                gold_grams=random.uniform(0, 5) if random.random() > 0.9 else 0,
                silver_grams=random.uniform(0, 50) if random.random() > 0.8 else 0,
                notes=f"Sample entry for {entry_date}",
            )
            db.add(entry)
        print(f"✓ Created 30 daily entries")
        
        # Create sample investments
        investments_data = [
            {"type": InvestmentType.GOLD, "name": "Gold Coins", "amount": 5000, "quantity": 5},
            {"type": InvestmentType.SILVER, "name": "Silver Bars", "amount": 3000, "quantity": 100},
            {"type": InvestmentType.STOCKS, "name": "AAPL", "amount": 10000, "quantity": 50},
            {"type": InvestmentType.CRYPTO, "name": "Bitcoin", "amount": 20000, "quantity": 0.5},
            {"type": InvestmentType.ETF, "name": "S&P 500 ETF", "amount": 15000, "quantity": 30},
        ]
        
        for inv_data in investments_data:
            investment = Investment(
                user_id=demo_user.id,
                investment_type=inv_data["type"],
                name=inv_data["name"],
                amount=inv_data["amount"],
                quantity=inv_data["quantity"],
                purchase_date=date.today() - timedelta(days=random.randint(30, 365)),
                current_value=inv_data["amount"] * random.uniform(0.9, 1.3),
            )
            db.add(investment)
        print(f"✓ Created {len(investments_data)} investments")
        
        # Create monthly goals
        today = date.today()
        goal = MonthlyGoal(
            user_id=demo_user.id,
            year=today.year,
            month=today.month,
            income_goal=20000,
            gold_goal=10,
            silver_goal=500,
            investment_goal=5100,
        )
        db.add(goal)
        print(f"✓ Created monthly goal for {today.year}-{today.month:02d}")
        
        await db.commit()
        print("\n✓ Database seeded successfully!")


if __name__ == "__main__":
    asyncio.run(seed_database())
