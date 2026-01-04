#!/usr/bin/env python3
"""Create superuser script."""
import asyncio
import sys
from getpass import getpass

from app.core.database import AsyncSessionLocal
from app.core.security import get_password_hash
from app.models.user import User


async def create_superuser():
    """Create a superuser interactively."""
    print("=== Create Superuser ===\n")
    
    email = input("Email: ").strip()
    username = input("Username: ").strip()
    full_name = input("Full name (optional): ").strip() or None
    password = getpass("Password: ")
    password_confirm = getpass("Confirm password: ")
    
    if password != password_confirm:
        print("Error: Passwords do not match!")
        sys.exit(1)
    
    async with AsyncSessionLocal() as db:
        # Check if user exists
        from sqlalchemy import select
        result = await db.execute(
            select(User).where(User.email == email)
        )
        if result.scalar_one_or_none():
            print(f"Error: User with email {email} already exists!")
            sys.exit(1)
        
        result = await db.execute(
            select(User).where(User.username == username)
        )
        if result.scalar_one_or_none():
            print(f"Error: User with username {username} already exists!")
            sys.exit(1)
        
        # Create superuser
        user = User(
            email=email,
            username=username,
            full_name=full_name,
            hashed_password=get_password_hash(password),
            is_active=True,
            is_superuser=True,
        )
        
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        print(f"\n✓ Superuser created successfully!")
        print(f"  Email: {user.email}")
        print(f"  Username: {user.username}")
        print(f"  ID: {user.id}")


if __name__ == "__main__":
    asyncio.run(create_superuser())
