"""API v1 router."""
from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    users,
    daily_entries,
    investments,
    goals,
    analytics,
    notifications,
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(daily_entries.router, prefix="/entries", tags=["entries"])
api_router.include_router(investments.router, prefix="/investments", tags=["investments"])
api_router.include_router(goals.router, prefix="/goals", tags=["goals"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
