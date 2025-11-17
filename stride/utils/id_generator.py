"""
ID Generator - Generates unique sprint identifiers.

Format: SPRINT-XXXX where XXXX is a random alphanumeric string.
"""
import random
import string
from typing import Set


def generate_sprint_id(existing_ids: Set[str] = None) -> str:
    """
    Generate a unique sprint ID in the format SPRINT-XXXX.
    
    Args:
        existing_ids: Set of existing IDs to avoid collisions
        
    Returns:
        Unique sprint ID (e.g., "SPRINT-7K9P")
    """
    existing_ids = existing_ids or set()
    
    # Characters to use: uppercase letters and digits (excluding similar looking: 0, O, I, 1)
    chars = string.ascii_uppercase.replace('O', '').replace('I', '') + string.digits.replace('0', '').replace('1', '')
    
    max_attempts = 1000
    for _ in range(max_attempts):
        # Generate 4-character random code
        code = ''.join(random.choices(chars, k=4))
        sprint_id = f"SPRINT-{code}"
        
        if sprint_id not in existing_ids:
            return sprint_id
    
    # Fallback to longer ID if collisions persist
    code = ''.join(random.choices(chars, k=6))
    return f"SPRINT-{code}"


def validate_sprint_id(sprint_id: str) -> bool:
    """
    Validate sprint ID format.
    
    Args:
        sprint_id: Sprint ID to validate
        
    Returns:
        True if valid format, False otherwise
    """
    if not sprint_id.startswith("SPRINT-"):
        return False
    
    code = sprint_id[7:]  # Remove "SPRINT-" prefix
    
    if len(code) < 4:
        return False
    
    # Check if code contains only alphanumeric characters
    return code.isalnum() and code.isupper()
