"""
ConfigManager - Handles Stride configuration management.

Manages both project-level and user-level configuration.
"""
from pathlib import Path
from typing import Optional, Dict, Any, List
import yaml
import json


class ConfigManager:
    """Manages Stride configuration at project and user levels."""
    
    # Default configuration structure
    DEFAULT_CONFIG = {
        "project": {
            "name": "",
            "version": "0.1.0",
            "agents": [],
            "validation": {
                "enabled": True,
                "strict_mode": False,
                "auto_lint": False,
                "auto_test": False,
            }
        },
        "user": {
            "email": "",
            "name": "",
        },
        "sprint": {
            "default_duration_days": 14,
            "auto_retrospective": True,
        }
    }
    
    def __init__(self, project_root: Optional[Path] = None) -> None:
        """
        Initialize the ConfigManager.
        
        Args:
            project_root: Root directory of the project. Defaults to current directory.
        """
        self.project_root = project_root or Path.cwd()
        self.project_config_path = self.project_root / "stride" / "config" / "stride.yaml"
        self.user_config_path = Path.home() / ".stride" / "config.yaml"
        
    def ensure_config_structure(self) -> None:
        """Ensure configuration directories exist."""
        # Project config directory
        self.project_config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # User config directory
        self.user_config_path.parent.mkdir(parents=True, exist_ok=True)
    
    def init_project_config(
        self,
        project_name: str,
        agents: Optional[List[str]] = None
    ) -> None:
        """
        Initialize project configuration with defaults.
        
        Args:
            project_name: Name of the project
            agents: List of AI agents to configure
        """
        self.ensure_config_structure()
        
        config = self.DEFAULT_CONFIG.copy()
        config["project"]["name"] = project_name
        config["project"]["agents"] = agents or []
        
        self._write_yaml(self.project_config_path, config)
    
    def init_user_config(self, email: str, name: str) -> None:
        """
        Initialize user configuration.
        
        Args:
            email: User email
            name: User name
        """
        self.ensure_config_structure()
        
        if self.user_config_path.exists():
            config = self._read_yaml(self.user_config_path) or {}
        else:
            config = {"user": {}}
        
        config["user"]["email"] = email
        config["user"]["name"] = name
        
        self._write_yaml(self.user_config_path, config)
    
    def get_project_config(self) -> Dict[str, Any]:
        """
        Get project configuration.
        
        Returns:
            Project configuration dictionary
        """
        if not self.project_config_path.exists():
            return self.DEFAULT_CONFIG.copy()
        
        config = self._read_yaml(self.project_config_path)
        return config if config else self.DEFAULT_CONFIG.copy()
    
    def get_user_config(self) -> Dict[str, Any]:
        """
        Get user configuration.
        
        Returns:
            User configuration dictionary
        """
        if not self.user_config_path.exists():
            return {"user": {"email": "", "name": ""}}
        
        config = self._read_yaml(self.user_config_path)
        return config if config else {"user": {"email": "", "name": ""}}
    
    def get_user_info(self) -> tuple[str, str]:
        """
        Get current user information.
        
        Returns:
            Tuple of (email, name)
        """
        config = self.get_user_config()
        user = config.get("user", {})
        return (user.get("email", ""), user.get("name", ""))
    
    def is_user_authenticated(self) -> bool:
        """
        Check if user is authenticated (has email configured).
        
        Returns:
            True if user email is set, False otherwise
        """
        email, _ = self.get_user_info()
        return bool(email)
    
    def update_project_config(self, updates: Dict[str, Any]) -> None:
        """
        Update project configuration.
        
        Args:
            updates: Dictionary of configuration updates
        """
        config = self.get_project_config()
        self._deep_update(config, updates)
        self._write_yaml(self.project_config_path, config)
    
    def add_agent(self, agent_name: str) -> None:
        """
        Add an AI agent to project configuration.
        
        Args:
            agent_name: Name of the agent to add
        """
        config = self.get_project_config()
        agents = config.get("project", {}).get("agents", [])
        
        if agent_name not in agents:
            agents.append(agent_name)
            self.update_project_config({"project": {"agents": agents}})
    
    def remove_agent(self, agent_name: str) -> bool:
        """
        Remove an AI agent from project configuration.
        
        Args:
            agent_name: Name of the agent to remove
            
        Returns:
            True if agent was removed, False if not found
        """
        config = self.get_project_config()
        agents = config.get("project", {}).get("agents", [])
        
        if agent_name in agents:
            agents.remove(agent_name)
            self.update_project_config({"project": {"agents": agents}})
            return True
        return False
    
    def get_agents(self) -> List[str]:
        """
        Get list of configured AI agents.
        
        Returns:
            List of agent names
        """
        config = self.get_project_config()
        return config.get("project", {}).get("agents", [])
    
    @staticmethod
    def _read_yaml(file_path: Path) -> Optional[Dict[str, Any]]:
        """Read YAML file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except (yaml.YAMLError, FileNotFoundError):
            return None
    
    @staticmethod
    def _write_yaml(file_path: Path, data: Dict[str, Any]) -> None:
        """Write data to YAML file."""
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
    
    @staticmethod
    def _deep_update(base: Dict[str, Any], updates: Dict[str, Any]) -> None:
        """Deep update dictionary recursively."""
        for key, value in updates.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                ConfigManager._deep_update(base[key], value)
            else:
                base[key] = value
