"""Auth tests."""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.auth import auth_service
from app.core.security import verify_password
from app.core.exceptions import AuthenticationError, ConflictError
from app.schemas.user import UserCreate, UserLogin


@pytest.mark.asyncio
async def test_register_user(db: AsyncSession, test_user_data):
    """Test user registration."""
    user_create = UserCreate(**test_user_data)
    user = await auth_service.register(db, user_create)
    
    assert user.email == test_user_data["email"]
    assert user.username == test_user_data["username"]
    assert user.full_name == test_user_data["full_name"]
    assert verify_password(test_user_data["password"], user.hashed_password)
    assert user.is_active is True
    assert user.is_superuser is False


@pytest.mark.asyncio
async def test_register_duplicate_email(db: AsyncSession, test_user_data):
    """Test registration with duplicate email."""
    user_create = UserCreate(**test_user_data)
    await auth_service.register(db, user_create)
    
    # Try to register again with same email
    with pytest.raises(ConflictError):
        await auth_service.register(db, user_create)


@pytest.mark.asyncio
async def test_login_success(db: AsyncSession, test_user_data):
    """Test successful login."""
    # Register user first
    user_create = UserCreate(**test_user_data)
    await auth_service.register(db, user_create)
    
    # Login
    user_login = UserLogin(
        username=test_user_data["username"],
        password=test_user_data["password"]
    )
    user, tokens = await auth_service.login(db, user_login)
    
    assert user.username == test_user_data["username"]
    assert tokens.access_token is not None
    assert tokens.refresh_token is not None
    assert tokens.token_type == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(db: AsyncSession, test_user_data):
    """Test login with invalid credentials."""
    user_login = UserLogin(
        username="nonexistent",
        password="wrongpassword"
    )
    
    with pytest.raises(AuthenticationError):
        await auth_service.login(db, user_login)


@pytest.mark.asyncio
async def test_refresh_token(db: AsyncSession, test_user_data):
    """Test token refresh."""
    # Register and login
    user_create = UserCreate(**test_user_data)
    await auth_service.register(db, user_create)
    
    user_login = UserLogin(
        username=test_user_data["username"],
        password=test_user_data["password"]
    )
    user, tokens = await auth_service.login(db, user_login)
    
    # Refresh token
    new_tokens = await auth_service.refresh_token(db, tokens.refresh_token)
    
    assert new_tokens.access_token is not None
    assert new_tokens.refresh_token is not None
    assert new_tokens.access_token != tokens.access_token
