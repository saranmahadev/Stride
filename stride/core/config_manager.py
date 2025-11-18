"""
ConfigManager - Handles Stride configuration management.

Manages both project-level and user-level configuration with validation and schema support.
"""
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple, Union
import yaml
import json
import logging
import re
import copy

logger = logging.getLogger(__name__)


class ConfigError(Exception):
    """Base exception for configuration errors."""
    pass


class ConfigValidationError(ConfigError):
    """Exception raised when configuration validation fails."""
    pass


class ConfigManager:
    """
    Manages Stride configuration at project and user levels.
    
    Supports:
    - User-level config (~/.stride/config.yaml)
    - Project-level config (stride.config.yaml)
    - YAML and JSON formats
    - Schema validation
    - Configuration merging
    - Dot notation for nested access
    """
    
    # Default user configuration
    DEFAULT_USER_CONFIG = {
        "user": {
            "name": None,
            "email": None
        },
        "defaults": {
            "priority": "medium",
            "tags": [],
            "format": "table"
        },
        "editor": {
            "preferred": None
        },
        "templates": {
            "custom_path": None
        }
    }
    
    # Default project configuration
    DEFAULT_PROJECT_CONFIG = {
        "project": {
            "name": "",
            "version": "1.0.0",
            "agents": []  # Keep agents under project for backward compatibility
        },
        "validation": {
            "strict": False,
            "require_tests": True,
            "require_docs": True
        },
        "sprint": {
            "default_priority": "medium",
            "auto_archive_after_days": 90
        },
        "templates": {
            "path": None
        },
        "paths": {
            "sprints": "./sprints",
            "specs": "./docs/specs"
        }
    }
    
    # Legacy default config for backward compatibility
    DEFAULT_CONFIG = DEFAULT_PROJECT_CONFIG
    
    def __init__(self, project_root: Optional[Path] = None) -> None:
        """
        Initialize the ConfigManager.
        
        Args:
            project_root: Root directory of the project. Defaults to current directory.
        """
        self.project_root = project_root or Path.cwd()
        self.project_config_path = self.project_root / "stride.config.yaml"
        self.user_config_path = Path.home() / ".stride" / "config.yaml"
        
        # Cache for loaded configs
        self._user_config: Optional[Dict] = None
        self._project_config: Optional[Dict] = None
        self._merged_config: Optional[Dict] = None
        
    def ensure_config_structure(self) -> None:
        """Ensure configuration directories exist."""
        # Project config directory
        self.project_config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # User config directory
        self.user_config_path.parent.mkdir(parents=True, exist_ok=True)
    
    def init_project_config(
        self,
        project_name: Optional[str] = None,
        agents: Optional[List[str]] = None,
        force: bool = False,
        **kwargs
    ) -> Path:
        """
        Initialize project configuration with defaults.
        
        Args:
            project_name: Name of the project
            agents: List of AI agents to configure
            force: Overwrite existing config
            **kwargs: Additional config values (supports dot notation)
            
        Returns:
            Path to created config file
        """
        if self.project_config_path.exists() and not force:
            raise ConfigError(
                f"Project config already exists: {self.project_config_path}\n"
                "Use force=True to overwrite"
            )
        
        self.ensure_config_structure()
        config = copy.deepcopy(self.DEFAULT_PROJECT_CONFIG)
        
        if project_name:
            config["project"]["name"] = project_name
        if agents:
            config["project"]["agents"] = agents
        
        # Apply any overrides from kwargs
        for key, value in kwargs.items():
            if "." in key:
                # Handle nested keys like "project.name"
                keys = key.split(".")
                current = config
                for k in keys[:-1]:
                    if k not in current:
                        current[k] = {}
                    current = current[k]
                current[keys[-1]] = value
            else:
                config[key] = value
        
        self.save_config(self.project_config_path, config)
        self._clear_cache()
        
        return self.project_config_path
    
    def init_user_config(self, email: Optional[str] = None, name: Optional[str] = None, force: bool = False) -> Path:
        """
        Initialize user configuration file.
        
        Args:
            email: User email (optional)
            name: User name (optional)
            force: Overwrite existing config
            
        Returns:
            Path to created config file
        """
        if self.user_config_path.exists() and not force:
            raise ConfigError(
                f"User config already exists: {self.user_config_path}\n"
                "Use force=True to overwrite"
            )
        
        self.ensure_config_structure()
        config = copy.deepcopy(self.DEFAULT_USER_CONFIG)
        
        if email:
            config["user"]["email"] = email
        if name:
            config["user"]["name"] = name
        
        self.save_config(self.user_config_path, config)
        self._clear_cache()
        
        return self.user_config_path
    
    def get_project_config(self) -> Dict[str, Any]:
        """
        Get project configuration with caching.
        
        Returns:
            Project configuration dictionary
        """
        if self._project_config is None:
            if not self.project_config_path.exists():
                self._project_config = copy.deepcopy(self.DEFAULT_PROJECT_CONFIG)
            else:
                config = self._read_yaml(self.project_config_path)
                self._project_config = config if config else copy.deepcopy(self.DEFAULT_PROJECT_CONFIG)
        
        return self._project_config
    
    def get_user_config(self) -> Dict[str, Any]:
        """
        Get user configuration with caching.
        
        Returns:
            User configuration dictionary
        """
        if self._user_config is None:
            if not self.user_config_path.exists():
                self._user_config = copy.deepcopy(self.DEFAULT_USER_CONFIG)
            else:
                config = self._read_yaml(self.user_config_path)
                self._user_config = config if config else copy.deepcopy(self.DEFAULT_USER_CONFIG)
        
        return self._user_config
    
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
        self._clear_cache()
    
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
    
    def load_config(self, config_path: Path, create_if_missing: bool = False) -> Dict:
        """
        Load configuration from file.
        
        Args:
            config_path: Path to configuration file
            create_if_missing: Create default config if file doesn't exist
            
        Returns:
            Configuration dictionary
            
        Raises:
            ConfigError: If file cannot be read or parsed
        """
        if not config_path.exists():
            if create_if_missing:
                logger.info(f"Config file not found, creating default: {config_path}")
                default_config = self._get_default_config(config_path)
                self.save_config(config_path, default_config)
                return default_config
            else:
                logger.warning(f"Config file not found: {config_path}")
                return {}
        
        try:
            content = config_path.read_text(encoding="utf-8")
            
            # Determine format by extension
            if config_path.suffix == ".json":
                config = json.loads(content)
            else:  # Default to YAML
                config = yaml.safe_load(content) or {}
            
            logger.info(f"Loaded config from: {config_path}")
            return config
            
        except json.JSONDecodeError as e:
            raise ConfigError(f"Invalid JSON in {config_path}: {e}")
        except yaml.YAMLError as e:
            raise ConfigError(f"Invalid YAML in {config_path}: {e}")
        except Exception as e:
            raise ConfigError(f"Failed to load config from {config_path}: {e}")
    
    def save_config(self, config_path: Path, data: Dict) -> None:
        """
        Save configuration to file.
        
        Args:
            config_path: Path to configuration file
            data: Configuration data to save
            
        Raises:
            ConfigError: If file cannot be written
        """
        try:
            # Create parent directory if needed
            config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Determine format by extension
            if config_path.suffix == ".json":
                content = json.dumps(data, indent=2)
            else:  # Default to YAML
                content = yaml.dump(data, default_flow_style=False, sort_keys=False)
            
            config_path.write_text(content, encoding="utf-8")
            logger.info(f"Saved config to: {config_path}")
            
        except Exception as e:
            raise ConfigError(f"Failed to save config to {config_path}: {e}")
    
    def validate_config(
        self,
        config: Dict,
        schema: Dict,
        strict: bool = False
    ) -> Tuple[bool, List[str]]:
        """
        Validate configuration against schema.
        
        Args:
            config: Configuration to validate
            schema: Schema definition
            strict: If True, fail on warnings
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        warnings = []
        
        def validate_value(value: Any, spec: Dict, path: str) -> None:
            """Validate a single value against its specification."""
            # Check required
            if spec.get("required", False) and value is None:
                errors.append(f"Missing required field: {path}")
                return
            
            if value is None:
                return  # Optional field not provided
            
            # Check type
            expected_type = spec.get("type")
            if expected_type:
                if expected_type == "string" and not isinstance(value, str):
                    errors.append(f"{path}: expected string, got {type(value).__name__}")
                elif expected_type == "integer" and not isinstance(value, int):
                    errors.append(f"{path}: expected integer, got {type(value).__name__}")
                elif expected_type == "boolean" and not isinstance(value, bool):
                    errors.append(f"{path}: expected boolean, got {type(value).__name__}")
                elif expected_type == "array" and not isinstance(value, list):
                    errors.append(f"{path}: expected array, got {type(value).__name__}")
                elif expected_type == "object" and not isinstance(value, dict):
                    errors.append(f"{path}: expected object, got {type(value).__name__}")
            
            # Check enum
            if "enum" in spec and value not in spec["enum"]:
                errors.append(
                    f"{path}: invalid value '{value}', must be one of: {', '.join(spec['enum'])}"
                )
            
            # Check pattern
            if "pattern" in spec and isinstance(value, str):
                pattern = spec["pattern"]
                if pattern == "email":
                    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value):
                        errors.append(f"{path}: invalid email format")
                elif not re.match(pattern, value):
                    errors.append(f"{path}: value doesn't match pattern {pattern}")
            
            # Check array items
            if expected_type == "array" and "items" in spec and isinstance(value, list):
                items_spec = spec["items"]
                if isinstance(items_spec, str):
                    # Simple type validation
                    for i, item in enumerate(value):
                        if items_spec == "string" and not isinstance(item, str):
                            errors.append(f"{path}[{i}]: expected string")
                elif isinstance(items_spec, dict):
                    # Complex object validation
                    for i, item in enumerate(value):
                        if isinstance(item, dict):
                            validate_object(item, items_spec, f"{path}[{i}]")
            
            # Check min/max
            if "min" in spec and isinstance(value, (int, float)) and value < spec["min"]:
                errors.append(f"{path}: value {value} is less than minimum {spec['min']}")
            if "max" in spec and isinstance(value, (int, float)) and value > spec["max"]:
                errors.append(f"{path}: value {value} is greater than maximum {spec['max']}")
        
        def validate_object(obj: Dict, schema_obj: Dict, prefix: str = "") -> None:
            """Recursively validate an object."""
            for key, spec in schema_obj.items():
                path = f"{prefix}.{key}" if prefix else key
                value = obj.get(key)
                
                if isinstance(spec, dict):
                    if "type" in spec:
                        # This is a leaf specification
                        validate_value(value, spec, path)
                    else:
                        # This is a nested object
                        if value is not None:
                            if not isinstance(value, dict):
                                errors.append(f"{path}: expected object, got {type(value).__name__}")
                            else:
                                validate_object(value, spec, path)
                        elif spec.get("required", False):
                            errors.append(f"Missing required field: {path}")
        
        # Validate the config
        validate_object(config, schema)
        
        # Combine errors and warnings
        all_issues = errors + (warnings if strict else [])
        is_valid = len(all_issues) == 0
        
        return is_valid, all_issues
    
    def merge_configs(self, base: Dict, override: Dict) -> Dict:
        """
        Merge two configurations, with override taking precedence.
        
        Args:
            base: Base configuration
            override: Override configuration
            
        Returns:
            Merged configuration
        """
        result = base.copy()
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                # Recursively merge nested dicts
                result[key] = self.merge_configs(result[key], value)
            else:
                # Override value
                result[key] = value
        
        return result
    
    def get_value(self, key_path: str, config: Optional[Dict] = None) -> Any:
        """
        Get configuration value using dot notation.
        
        Args:
            key_path: Dot-separated path (e.g., "user.name")
            config: Configuration dict (default: merged config)
            
        Returns:
            Configuration value or None if not found
            
        Example:
            >>> config.get_value("user.name")
            "John Doe"
        """
        if config is None:
            config = self.get_merged_config()
        
        keys = key_path.split(".")
        value = config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return None
        
        return value
    
    def set_value(
        self,
        key_path: str,
        value: Any,
        config_type: str = "user"
    ) -> None:
        """
        Set configuration value using dot notation.
        
        Args:
            key_path: Dot-separated path (e.g., "user.name")
            value: Value to set
            config_type: "user" or "project"
            
        Raises:
            ConfigError: If path is invalid
            
        Example:
            >>> config.set_value("user.name", "John Doe")
        """
        # Load the appropriate config
        if config_type == "user":
            config_path = self.user_config_path
            config = self.get_user_config()
        elif config_type == "project":
            config_path = self.project_config_path
            config = self.get_project_config()
        else:
            raise ConfigError(f"Invalid config type: {config_type}")
        
        # Navigate to the parent of the target key
        keys = key_path.split(".")
        current = config
        
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            elif not isinstance(current[key], dict):
                raise ConfigError(f"Cannot set {key_path}: {key} is not an object")
            current = current[key]
        
        # Set the value
        current[keys[-1]] = value
        
        # Save the config
        self.save_config(config_path, config)
        
        # Clear cache
        self._clear_cache()
        
        logger.info(f"Set {config_type} config: {key_path} = {value}")
    
    def get_merged_config(self) -> Dict:
        """
        Get merged configuration (user + project).
        
        Project config overrides user config.
        
        Returns:
            Merged configuration dictionary
        """
        if self._merged_config is None:
            user_config = self.get_user_config()
            project_config = self.get_project_config()
            self._merged_config = self.merge_configs(user_config, project_config)
        
        return self._merged_config
    
    def reset_config(self, config_type: str) -> None:
        """
        Reset configuration to defaults.
        
        Args:
            config_type: "user" or "project"
        """
        if config_type == "user":
            self.save_config(self.user_config_path, copy.deepcopy(self.DEFAULT_USER_CONFIG))
        elif config_type == "project":
            self.save_config(self.project_config_path, copy.deepcopy(self.DEFAULT_PROJECT_CONFIG))
        else:
            raise ConfigError(f"Invalid config type: {config_type}")
        
        self._clear_cache()
    
    def _get_default_config(self, config_path: Path) -> Dict:
        """Get default config based on path."""
        if "stride.config" in config_path.name:
            return copy.deepcopy(self.DEFAULT_PROJECT_CONFIG)
        else:
            return copy.deepcopy(self.DEFAULT_USER_CONFIG)
    
    def _clear_cache(self) -> None:
        """Clear cached configurations."""
        self._user_config = None
        self._project_config = None
        self._merged_config = None
    
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
