"""
Base Tool Configurator Interface

Defines the interface that all AI tool configurators must implement.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class ConfigResult:
    """Result of a configuration operation."""
    success: bool
    messages: List[str]
    files_created: List[Path] = None
    
    def __post_init__(self):
        if self.files_created is None:
            self.files_created = []


@dataclass
class ValidationResult:
    """Result of a validation check."""
    valid: bool
    issues: List[str]
    warnings: List[str] = None
    
    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []


class ToolConfigurator(ABC):
    """
    Base class for AI tool configurators.
    
    Each tool (Claude, Cursor, etc.) has a configurator that knows how to:
    - Create root config files
    - Generate slash command prompts
    - Validate integration health
    - Update managed blocks
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable tool name (e.g., 'Claude Code')."""
        pass
    
    @property
    @abstractmethod
    def slug(self) -> str:
        """Short identifier (e.g., 'claude')."""
        pass
    
    @property
    @abstractmethod
    def config_file_name(self) -> Optional[str]:
        """Root config filename (e.g., 'CLAUDE.md') or None if not needed."""
        pass
    
    @property
    @abstractmethod
    def slash_command_dir(self) -> Optional[str]:
        """
        Slash command directory (e.g., '.claude/prompts/') or None.
        Relative to project root.
        """
        pass
    
    @property
    @abstractmethod
    def command_format(self) -> Optional[str]:
        """
        Slash command file format: 'toml' or 'markdown' or None.
        """
        pass
    
    @property
    def priority(self) -> str:
        """
        Integration priority: 'high', 'medium', or 'low'.
        Default is 'medium'.
        """
        return 'medium'
    
    @property
    def integration_type(self) -> str:
        """
        Type of integration:
        - 'root_only': Just creates root config file
        - 'slash_only': Just creates slash commands
        - 'hybrid': Creates both root config and slash commands
        """
        if self.config_file_name and self.slash_command_dir:
            return 'hybrid'
        elif self.config_file_name:
            return 'root_only'
        elif self.slash_command_dir:
            return 'slash_only'
        return 'unknown'
    
    @abstractmethod
    def configure(self, project_path: Path) -> ConfigResult:
        """
        Set up tool integration files.
        
        Args:
            project_path: Root directory of the project
            
        Returns:
            ConfigResult with success status and messages
        """
        pass
    
    @abstractmethod
    def validate(self, project_path: Path) -> ValidationResult:
        """
        Validate that integration is correctly configured.
        
        Args:
            project_path: Root directory of the project
            
        Returns:
            ValidationResult with any issues found
        """
        pass
    
    @abstractmethod
    def update(self, project_path: Path) -> ConfigResult:
        """
        Update managed blocks with latest templates.
        
        Args:
            project_path: Root directory of the project
            
        Returns:
            ConfigResult with update status
        """
        pass
    
    def get_info(self) -> Dict[str, str]:
        """
        Get information about this tool configurator.
        
        Returns:
            Dictionary with tool metadata
        """
        return {
            'name': self.name,
            'slug': self.slug,
            'type': self.integration_type,
            'priority': self.priority,
            'config_file': self.config_file_name or 'None',
            'slash_dir': self.slash_command_dir or 'None',
            'format': self.command_format or 'None'
        }
