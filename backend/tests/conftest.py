"""Test configuration."""
import pytest
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.core.config import settings
from app.core.database import Base
from app.models import *  # noqa


# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://portfel:portfel_password@localhost:5432/portfel_test_db"

# Create test engine
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)

# Create test session factory
TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def db() -> AsyncGenerator[AsyncSession, None]:
    """Create test database session."""
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session
    async with TestSessionLocal() as session:
        yield session
    
    # Drop tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def test_user_data():
    """Test user data."""
    return {
        "email": "test@test.com",
        "username": "testuser",
        "full_name": "Test User",
        "password": "testpassword123",
    }
