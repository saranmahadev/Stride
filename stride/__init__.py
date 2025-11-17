"""
Stride - Sprint-Powered, Spec-Driven Development for AI Agents

A framework that combines OpenSpec's clarity, SpecKit's rigor, and agile velocity
into a unified workflow for AI-assisted development.
"""

__version__ = "0.1.0"
__author__ = "Stride Development Team"

from stride.core.folder_manager import FolderManager
from stride.core.sprint_manager import SprintManager
from stride.core.config_manager import ConfigManager

__all__ = [
    "FolderManager",
    "SprintManager",
    "ConfigManager",
]
