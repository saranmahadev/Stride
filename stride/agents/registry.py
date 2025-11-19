"""
Tool Registry for AI Agent Configurators

Central registry for all available AI tool configurators.
Provides discovery, lookup, and management of tool integrations.
"""

from typing import Dict, List, Optional
from .configurator import ToolConfigurator


class ToolRegistry:
    """
    Central registry of all AI tool configurators.
    
    Tools are auto-registered on import of their configurator modules.
    """
    
    _tools: Dict[str, ToolConfigurator] = {}
    
    @classmethod
    def register(cls, configurator: ToolConfigurator) -> None:
        """
        Register a tool configurator.
        
        Args:
            configurator: ToolConfigurator instance to register
        """
        slug = configurator.slug.lower()
        if slug in cls._tools:
            raise ValueError(f"Tool '{slug}' is already registered")
        cls._tools[slug] = configurator
    
    @classmethod
    def unregister(cls, slug: str) -> bool:
        """
        Unregister a tool configurator.
        
        Args:
            slug: Tool slug to unregister
            
        Returns:
            True if tool was unregistered, False if not found
        """
        slug = slug.lower()
        if slug in cls._tools:
            del cls._tools[slug]
            return True
        return False
    
    @classmethod
    def get(cls, slug: str) -> Optional[ToolConfigurator]:
        """
        Get a tool configurator by slug.
        
        Args:
            slug: Tool slug (e.g., 'claude', 'cursor')
            
        Returns:
            ToolConfigurator instance or None if not found
        """
        return cls._tools.get(slug.lower())
    
    @classmethod
    def list_all(cls) -> List[ToolConfigurator]:
        """
        Get all registered tool configurators.
        
        Returns:
            List of all ToolConfigurator instances
        """
        return list(cls._tools.values())
    
    @classmethod
    def list_by_priority(cls, priority: str) -> List[ToolConfigurator]:
        """
        Get tools filtered by priority level.
        
        Args:
            priority: Priority level ('high', 'medium', or 'low')
            
        Returns:
            List of matching ToolConfigurator instances
        """
        return [tool for tool in cls._tools.values() if tool.priority == priority]
    
    @classmethod
    def list_by_type(cls, integration_type: str) -> List[ToolConfigurator]:
        """
        Get tools filtered by integration type.
        
        Args:
            integration_type: Type ('root_only', 'slash_only', 'hybrid')
            
        Returns:
            List of matching ToolConfigurator instances
        """
        return [tool for tool in cls._tools.values() if tool.integration_type == integration_type]
    
    @classmethod
    def get_count(cls) -> int:
        """Get total number of registered tools."""
        return len(cls._tools)
    
    @classmethod
    def clear(cls) -> None:
        """Clear all registered tools (mainly for testing)."""
        cls._tools.clear()
    
    @classmethod
    def get_summary(cls) -> Dict[str, int]:
        """
        Get summary statistics of registered tools.
        
        Returns:
            Dictionary with counts by priority and type
        """
        tools = cls.list_all()
        return {
            'total': len(tools),
            'high_priority': len([t for t in tools if t.priority == 'high']),
            'medium_priority': len([t for t in tools if t.priority == 'medium']),
            'low_priority': len([t for t in tools if t.priority == 'low']),
            'root_only': len([t for t in tools if t.integration_type == 'root_only']),
            'slash_only': len([t for t in tools if t.integration_type == 'slash_only']),
            'hybrid': len([t for t in tools if t.integration_type == 'hybrid'])
        }
