"""Helper utilities."""
from datetime import datetime, date
from typing import Any, Dict


def get_current_month() -> tuple[int, int]:
    """
    Get current year and month.
    
    Returns:
        Tuple of (year, month)
    """
    now = datetime.now()
    return now.year, now.month


def format_currency(amount: float, currency: str = "PLN") -> str:
    """
    Format currency amount.
    
    Args:
        amount: Amount to format
        currency: Currency code
        
    Returns:
        Formatted currency string
    """
    return f"{amount:,.2f} {currency}"


def calculate_percentage(value: float, total: float) -> float:
    """
    Calculate percentage.
    
    Args:
        value: Value
        total: Total
        
    Returns:
        Percentage (0-100)
    """
    if total == 0:
        return 0.0
    return (value / total) * 100


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing unsafe characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    import re
    # Remove any character that's not alphanumeric, dash, underscore, or dot
    return re.sub(r'[^\w\-\.]', '_', filename)
