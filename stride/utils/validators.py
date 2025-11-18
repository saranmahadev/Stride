"""
Input validation utilities for Stride.
"""
import re
from typing import Tuple


# Email validation regex pattern
# Matches standard email format: user@domain.tld
EMAIL_REGEX = re.compile(
    r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
)


def validate_email(email: str) -> Tuple[bool, str]:
    """
    Validate email address format.
    
    Args:
        email: Email address to validate
        
    Returns:
        Tuple of (is_valid, error_message)
        If valid, error_message is empty string
        
    Examples:
        >>> validate_email("user@example.com")
        (True, "")
        
        >>> validate_email("invalid")
        (False, "Invalid email format")
    """
    if not email:
        return False, "Email cannot be empty"
    
    # Remove leading/trailing whitespace
    email = email.strip()
    
    # Check length
    if len(email) < 3:
        return False, "Email is too short"
    
    if len(email) > 254:  # RFC 5321
        return False, "Email is too long (max 254 characters)"
    
    # Check basic format
    if '@' not in email:
        return False, "Email must contain '@'"
    
    # Check for multiple @
    if email.count('@') > 1:
        return False, "Email cannot contain multiple '@' symbols"
    
    # Split into local and domain parts
    local, domain = email.rsplit('@', 1)
    
    if not local:
        return False, "Email must have a username before '@'"
    
    if not domain:
        return False, "Email must have a domain after '@'"
    
    if '.' not in domain:
        return False, "Email domain must contain a '.'"
    
    # Check against regex pattern
    if not EMAIL_REGEX.match(email):
        return False, "Invalid email format. Expected format: user@domain.com"
    
    return True, ""


def validate_name(name: str) -> Tuple[bool, str]:
    """
    Validate user name.
    
    Args:
        name: User name to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name:
        return False, "Name cannot be empty"
    
    # Remove leading/trailing whitespace
    name = name.strip()
    
    if len(name) < 2:
        return False, "Name must be at least 2 characters"
    
    if len(name) > 100:
        return False, "Name is too long (max 100 characters)"
    
    return True, ""
