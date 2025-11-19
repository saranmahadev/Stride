"""
Stride AI Agent Integration Framework

This module provides the infrastructure for integrating Stride workflows
with 20+ AI coding assistants using managed configuration files and
native slash commands.

Key Components:
- Managed marker system for safe updates
- Template system for consistent workflow instructions
- Configurator pattern for tool-specific integrations
- Registry for managing available tools
"""

from .markers import ManagedMarkerSystem
from .templates import TemplateManager
from .registry import ToolRegistry
from .configurator import ToolConfigurator

__all__ = [
    'ManagedMarkerSystem',
    'TemplateManager',
    'ToolRegistry',
    'ToolConfigurator',
]
