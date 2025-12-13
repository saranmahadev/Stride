"""
Configuration management for Stride.
Handles reading/writing .stride/config.yaml and environment variables.

Note: Currently returns empty config. Configuration is managed through
.stride directory structure and agent-specific files.
"""

from typing import Any, Dict

# Supabase Configuration (Hardcoded - Not user-configurable)
SUPABASE_URL = "https://fzlnqnsiutubfcqfyjwf.supabase.co"
SUPABASE_PUBLISHABLE_KEY = "sb_publishable__6BzETxBn1lC2ESAF65IQg_8xJ4anzL"
REDIRECT_URI = "http://localhost:37777/callback"


def get_config() -> Dict[str, Any]:
    """
    Retrieve current configuration.

    Returns:
        Empty dict (configuration managed via .stride directory)
    """
    return {}
