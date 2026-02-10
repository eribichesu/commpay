"""
Utility Module

Helper functions and utilities for document generation.
"""

from datetime import datetime
from typing import Any, Dict


def format_currency(amount: float, currency: str = "EUR") -> str:
    """
    Format a monetary amount.
    
    Args:
        amount: Amount to format
        currency: Currency code (default: EUR)
        
    Returns:
        Formatted currency string
    """
    return f"{currency} {amount:.2f}"


def format_date(date: datetime, format_str: str = "%d/%m/%Y") -> str:
    """
    Format a date object.
    
    Args:
        date: Date to format
        format_str: Date format string
        
    Returns:
        Formatted date string
    """
    return date.strftime(format_str)


def validate_document_data(data: Dict[str, Any], required_fields: list[str]) -> bool:
    """
    Validate that all required fields are present in document data.
    
    Args:
        data: Document data dictionary
        required_fields: List of required field names
        
    Returns:
        True if all required fields are present, False otherwise
    """
    return all(field in data for field in required_fields)
