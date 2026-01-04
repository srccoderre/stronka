"""Custom exceptions for the application."""


class PortfelException(Exception):
    """Base exception for all application exceptions."""
    
    def __init__(self, message: str = "An error occurred", status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class AuthenticationError(PortfelException):
    """Authentication failed."""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=401)


class AuthorizationError(PortfelException):
    """User not authorized."""
    
    def __init__(self, message: str = "Not authorized"):
        super().__init__(message, status_code=403)


class NotFoundError(PortfelException):
    """Resource not found."""
    
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)


class ValidationError(PortfelException):
    """Validation error."""
    
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, status_code=422)


class ConflictError(PortfelException):
    """Resource conflict."""
    
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message, status_code=409)


class RateLimitError(PortfelException):
    """Rate limit exceeded."""
    
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, status_code=429)


class DatabaseError(PortfelException):
    """Database operation failed."""
    
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(message, status_code=500)
