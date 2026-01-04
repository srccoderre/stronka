"""Services initialization."""
from app.services.auth import AuthService, auth_service
from app.services.user import UserService, user_service
from app.services.finance import FinanceService, finance_service
from app.services.analytics import AnalyticsService, analytics_service
from app.services.notification import NotificationService, notification_service

__all__ = [
    "AuthService",
    "auth_service",
    "UserService",
    "user_service",
    "FinanceService",
    "finance_service",
    "AnalyticsService",
    "analytics_service",
    "NotificationService",
    "notification_service",
]
