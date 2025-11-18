"""
Tests for ConfigManager - comprehensive test suite for configuration management.
"""
import json
import pytest
import shutil
import tempfile
from pathlib import Path
from stride.core.config_manager import ConfigManager, ConfigError, ConfigValidationError
from stride.core.config_schemas import USER_CONFIG_SCHEMA, PROJECT_CONFIG_SCHEMA


@pytest.fixture
def temp_project(monkeypatch):
    """Create temporary project directory and mock home directory."""
    tmp = Path(tempfile.mkdtemp())
    tmp_home = tmp / "home"
    tmp_home.mkdir()
    
    # Mock Path.home() to return our temp home
    monkeypatch.setattr(Path, "home", lambda: tmp_home)
    
    yield tmp
    shutil.rmtree(tmp)


class TestConfigManagerBasics:
    """Test basic ConfigManager functionality."""
    
    def test_init(self, temp_project):
        """Test ConfigManager initialization."""
        cm = ConfigManager(temp_project)
        assert cm.project_root == temp_project
        assert cm.project_config_path == temp_project / "stride.config.yaml"
        assert cm.user_config_path == Path.home() / ".stride" / "config.yaml"
    
    def test_default_configs(self):
        """Test default configuration structures."""
        cm = ConfigManager()
        assert "user" in cm.DEFAULT_USER_CONFIG
        assert "defaults" in cm.DEFAULT_USER_CONFIG
        assert "project" in cm.DEFAULT_PROJECT_CONFIG
        assert "validation" in cm.DEFAULT_PROJECT_CONFIG


class TestConfigLoading:
    """Test configuration loading."""
    
    def test_load_yaml_config(self, temp_project):
        """Test loading YAML configuration."""
        cm = ConfigManager(temp_project)
        config_path = temp_project / "test.yaml"
        
        # Create test config
        test_config = {"test": "value", "nested": {"key": "data"}}
        cm.save_config(config_path, test_config)
        
        # Load and verify
        loaded = cm.load_config(config_path)
        assert loaded == test_config
    
    def test_load_json_config(self, temp_project):
        """Test loading JSON configuration."""
        cm = ConfigManager(temp_project)
        config_path = temp_project / "test.json"
        
        # Create test config
        test_config = {"test": "value", "nested": {"key": "data"}}
        cm.save_config(config_path, test_config)
        
        # Load and verify
        loaded = cm.load_config(config_path)
        assert loaded == test_config
    
    def test_load_missing_config(self, temp_project):
        """Test loading non-existent config."""
        cm = ConfigManager(temp_project)
        config_path = temp_project / "missing.yaml"
        
        loaded = cm.load_config(config_path)
        assert loaded == {}
    
    def test_load_config_create_if_missing(self, temp_project):
        """Test creating default config if missing."""
        cm = ConfigManager(temp_project)
        config_path = temp_project / "stride.config.yaml"
        
        loaded = cm.load_config(config_path, create_if_missing=True)
        assert config_path.exists()
        assert "project" in loaded
    
    def test_load_invalid_yaml(self, temp_project):
        """Test loading invalid YAML."""
        cm = ConfigManager(temp_project)
        config_path = temp_project / "bad.yaml"
        config_path.write_text("invalid: yaml: content: [[[")
        
        with pytest.raises(ConfigError, match="Invalid YAML"):
            cm.load_config(config_path)
    
    def test_load_invalid_json(self, temp_project):
        """Test loading invalid JSON."""
        cm = ConfigManager(temp_project)
        config_path = temp_project / "bad.json"
        config_path.write_text('{"invalid": json}')
        
        with pytest.raises(ConfigError, match="Invalid JSON"):
            cm.load_config(config_path)


class TestConfigSaving:
    """Test configuration saving."""
    
    def test_save_yaml_config(self, temp_project):
        """Test saving YAML configuration."""
        cm = ConfigManager(temp_project)
        config_path = temp_project / "test.yaml"
        test_config = {"key": "value", "number": 42}
        
        cm.save_config(config_path, test_config)
        
        assert config_path.exists()
        loaded = cm.load_config(config_path)
        assert loaded == test_config
    
    def test_save_json_config(self, temp_project):
        """Test saving JSON configuration."""
        cm = ConfigManager(temp_project)
        config_path = temp_project / "test.json"
        test_config = {"key": "value", "number": 42}
        
        cm.save_config(config_path, test_config)
        
        assert config_path.exists()
        content = config_path.read_text()
        assert json.loads(content) == test_config
    
    def test_save_creates_directories(self, temp_project):
        """Test that save creates parent directories."""
        cm = ConfigManager(temp_project)
        config_path = temp_project / "nested" / "dirs" / "config.yaml"
        
        cm.save_config(config_path, {"test": "value"})
        
        assert config_path.exists()


class TestConfigValidation:
    """Test configuration validation."""
    
    def test_validate_valid_config(self):
        """Test validating a valid configuration."""
        cm = ConfigManager()
        config = {
            "user": {"name": "John", "email": "john@example.com"},
            "defaults": {"priority": "high", "format": "table"}
        }
        
        is_valid, errors = cm.validate_config(config, USER_CONFIG_SCHEMA)
        assert is_valid
        assert len(errors) == 0
    
    def test_validate_missing_required_field(self):
        """Test validation with missing required field."""
        cm = ConfigManager()
        config = {
            "project": {},  # project exists but name is missing
            "validation": {"strict": True}
        }
        
        is_valid, errors = cm.validate_config(config, PROJECT_CONFIG_SCHEMA)
        assert not is_valid
        assert any("project.name" in err for err in errors)
    
    def test_validate_invalid_type(self):
        """Test validation with wrong type."""
        cm = ConfigManager()
        config = {
            "project": {"name": "Test", "version": 123}  # version should be string
        }
        
        is_valid, errors = cm.validate_config(config, PROJECT_CONFIG_SCHEMA)
        assert not is_valid
        assert any("version" in err and "string" in err for err in errors)
    
    def test_validate_invalid_enum(self):
        """Test validation with invalid enum value."""
        cm = ConfigManager()
        config = {
            "project": {"name": "Test"},
            "sprint": {"default_priority": "invalid"}  # Not in enum
        }
        
        is_valid, errors = cm.validate_config(config, PROJECT_CONFIG_SCHEMA)
        assert not is_valid
        assert any("default_priority" in err for err in errors)
    
    def test_validate_invalid_email(self):
        """Test validation with invalid email."""
        cm = ConfigManager()
        config = {
            "user": {"email": "not-an-email"}
        }
        
        is_valid, errors = cm.validate_config(config, USER_CONFIG_SCHEMA)
        assert not is_valid
        assert any("email" in err for err in errors)
    
    def test_validate_array_type(self):
        """Test validation of array types."""
        cm = ConfigManager()
        config = {
            "project": {"name": "Test"},
            "defaults": {"tags": ["tag1", "tag2"]}
        }
        
        is_valid, errors = cm.validate_config(config, USER_CONFIG_SCHEMA)
        assert is_valid
    
    def test_validate_min_max(self):
        """Test validation of min/max constraints."""
        cm = ConfigManager()
        
        # Test below minimum
        config1 = {
            "project": {"name": "Test"},
            "sprint": {"auto_archive_after_days": 0}
        }
        is_valid, errors = cm.validate_config(config1, PROJECT_CONFIG_SCHEMA)
        assert not is_valid
        assert any("minimum" in err for err in errors)
        
        # Test above maximum
        config2 = {
            "project": {"name": "Test"},
            "sprint": {"auto_archive_after_days": 500}
        }
        is_valid, errors = cm.validate_config(config2, PROJECT_CONFIG_SCHEMA)
        assert not is_valid
        assert any("maximum" in err for err in errors)


class TestConfigMerging:
    """Test configuration merging."""
    
    def test_merge_simple(self):
        """Test merging simple configurations."""
        cm = ConfigManager()
        base = {"a": 1, "b": 2}
        override = {"b": 3, "c": 4}
        
        result = cm.merge_configs(base, override)
        assert result == {"a": 1, "b": 3, "c": 4}
    
    def test_merge_nested(self):
        """Test merging nested configurations."""
        cm = ConfigManager()
        base = {"user": {"name": "John", "email": "john@example.com"}}
        override = {"user": {"email": "jane@example.com"}}
        
        result = cm.merge_configs(base, override)
        assert result["user"]["name"] == "John"
        assert result["user"]["email"] == "jane@example.com"
    
    def test_merge_deep_nested(self):
        """Test merging deeply nested configurations."""
        cm = ConfigManager()
        base = {
            "project": {
                "validation": {"strict": False, "require_tests": True}
            }
        }
        override = {
            "project": {
                "validation": {"strict": True}
            }
        }
        
        result = cm.merge_configs(base, override)
        assert result["project"]["validation"]["strict"] is True
        assert result["project"]["validation"]["require_tests"] is True


class TestDotNotation:
    """Test dot notation access."""
    
    def test_get_value_simple(self, temp_project):
        """Test getting simple value."""
        cm = ConfigManager(temp_project)
        config = {"user": {"name": "John"}}
        
        value = cm.get_value("user.name", config)
        assert value == "John"
    
    def test_get_value_nested(self, temp_project):
        """Test getting nested value."""
        cm = ConfigManager(temp_project)
        config = {
            "project": {
                "validation": {"strict": True}
            }
        }
        
        value = cm.get_value("project.validation.strict", config)
        assert value is True
    
    def test_get_value_missing(self, temp_project):
        """Test getting non-existent value."""
        cm = ConfigManager(temp_project)
        config = {"user": {"name": "John"}}
        
        value = cm.get_value("user.email", config)
        assert value is None
    
    def test_set_value_user(self, temp_project):
        """Test setting user config value."""
        cm = ConfigManager(temp_project)
        cm.init_user_config(force=True)
        
        cm.set_value("user.name", "Jane", config_type="user")
        
        value = cm.get_value("user.name")
        assert value == "Jane"
    
    def test_set_value_project(self, temp_project):
        """Test setting project config value."""
        cm = ConfigManager(temp_project)
        cm.init_project_config("Test", force=True)
        
        cm.set_value("project.version", "2.0.0", config_type="project")
        
        config = cm.get_project_config()
        assert config["project"]["version"] == "2.0.0"
    
    def test_set_value_nested(self, temp_project):
        """Test setting nested value."""
        cm = ConfigManager(temp_project)
        cm.init_project_config("Test", force=True)
        
        cm.set_value("validation.strict", True, config_type="project")
        
        value = cm.get_value("validation.strict")
        assert value is True
    
    def test_set_value_invalid_type(self, temp_project):
        """Test setting value with invalid config type."""
        cm = ConfigManager(temp_project)
        
        with pytest.raises(ConfigError, match="Invalid config type"):
            cm.set_value("key", "value", config_type="invalid")


class TestUserConfig:
    """Test user configuration management."""
    
    def test_init_user_config(self, temp_project):
        """Test initializing user config."""
        cm = ConfigManager(temp_project)
        
        path = cm.init_user_config(email="user@example.com", name="User", force=True)
        
        assert path.exists()
        config = cm.get_user_config()
        assert config["user"]["email"] == "user@example.com"
        assert config["user"]["name"] == "User"
    
    def test_init_user_config_already_exists(self, temp_project):
        """Test initializing user config when it already exists."""
        cm = ConfigManager(temp_project)
        cm.init_user_config(force=True)
        
        with pytest.raises(ConfigError, match="already exists"):
            cm.init_user_config()
    
    def test_get_user_config_default(self, temp_project):
        """Test getting user config when it doesn't exist."""
        cm = ConfigManager(temp_project)
        
        config = cm.get_user_config()
        assert "user" in config
        assert "defaults" in config


class TestProjectConfig:
    """Test project configuration management."""
    
    def test_init_project_config(self, temp_project):
        """Test initializing project config."""
        cm = ConfigManager(temp_project)
        
        path = cm.init_project_config(
            project_name="Test Project",
            agents=["Claude", "Copilot"],
            force=True
        )
        
        assert path.exists()
        config = cm.get_project_config()
        assert config["project"]["name"] == "Test Project"
        assert config["project"]["agents"] == ["Claude", "Copilot"]
    
    def test_init_project_config_with_kwargs(self, temp_project):
        """Test initializing project config with additional kwargs."""
        cm = ConfigManager(temp_project)
        
        cm.init_project_config(
            project_name="Test",
            force=True,
            **{"validation.strict": True}
        )
        
        config = cm.get_project_config()
        assert config["validation"]["strict"] is True
    
    def test_get_project_config_default(self, temp_project):
        """Test getting project config when it doesn't exist."""
        cm = ConfigManager(temp_project)
        
        config = cm.get_project_config()
        assert "project" in config
        assert "validation" in config


class TestConfigCaching:
    """Test configuration caching."""
    
    def test_user_config_cached(self, temp_project):
        """Test that user config is cached."""
        cm = ConfigManager(temp_project)
        cm.init_user_config(force=True)
        
        config1 = cm.get_user_config()
        config2 = cm.get_user_config()
        
        assert config1 is config2  # Same object due to caching
    
    def test_project_config_cached(self, temp_project):
        """Test that project config is cached."""
        cm = ConfigManager(temp_project)
        cm.init_project_config("Test", force=True)
        
        config1 = cm.get_project_config()
        config2 = cm.get_project_config()
        
        assert config1 is config2  # Same object due to caching
    
    def test_cache_cleared_on_save(self, temp_project):
        """Test that cache is cleared when config is saved."""
        cm = ConfigManager(temp_project)
        cm.init_user_config(force=True)
        
        config1 = cm.get_user_config()
        cm.set_value("user.name", "New Name", config_type="user")
        config2 = cm.get_user_config()
        
        assert config1 is not config2  # Cache was cleared


class TestMergedConfig:
    """Test merged configuration."""
    
    def test_get_merged_config(self, temp_project):
        """Test getting merged user + project config."""
        cm = ConfigManager(temp_project)
        cm.init_user_config(email="user@example.com", force=True)
        cm.init_project_config("Test Project", force=True)
        
        merged = cm.get_merged_config()
        
        assert "user" in merged
        assert "project" in merged
        assert merged["user"]["email"] == "user@example.com"
        assert merged["project"]["name"] == "Test Project"
    
    def test_project_overrides_user(self, temp_project):
        """Test that project config overrides user config."""
        cm = ConfigManager(temp_project)
        
        # Set user default priority
        cm.init_user_config(force=True)
        cm.set_value("defaults.priority", "low", config_type="user")
        
        # Set project default priority
        cm.init_project_config("Test", force=True)
        cm.set_value("sprint.default_priority", "high", config_type="project")
        
        merged = cm.get_merged_config()
        
        # Project value should be present
        assert merged["sprint"]["default_priority"] == "high"


class TestConfigReset:
    """Test configuration reset."""
    
    def test_reset_user_config(self, temp_project):
        """Test resetting user config to defaults."""
        cm = ConfigManager(temp_project)
        cm.init_user_config(email="test@example.com", name="User", force=True)
        cm.set_value("user.name", "Modified", config_type="user")
        
        # Verify it was modified
        config_before = cm.get_user_config()
        assert config_before["user"]["name"] == "Modified"
        
        # Reset to defaults
        cm.reset_config("user")
        
        config_after = cm.get_user_config()
        assert config_after["user"]["name"] is None  # Back to default
    
    def test_reset_project_config(self, temp_project):
        """Test resetting project config to defaults."""
        cm = ConfigManager(temp_project)
        cm.init_project_config("Test", force=True)
        cm.set_value("project.name", "Modified", config_type="project")
        
        cm.reset_config("project")
        
        config = cm.get_project_config()
        assert config["project"]["name"] == ""  # Back to default
    
    def test_reset_invalid_type(self, temp_project):
        """Test resetting with invalid type."""
        cm = ConfigManager(temp_project)
        
        with pytest.raises(ConfigError, match="Invalid config type"):
            cm.reset_config("invalid")


class TestBackwardCompatibility:
    """Test backward compatibility with existing code."""
    
    def test_get_user_info(self, temp_project):
        """Test get_user_info method."""
        cm = ConfigManager(temp_project)
        cm.init_user_config(email="user@example.com", name="User", force=True)
        
        email, name = cm.get_user_info()
        assert email == "user@example.com"
        assert name == "User"
    
    def test_is_user_authenticated(self, temp_project):
        """Test is_user_authenticated method."""
        cm = ConfigManager(temp_project)
        
        assert not cm.is_user_authenticated()
        
        cm.init_user_config(email="user@example.com", force=True)
        assert cm.is_user_authenticated()
    
    def test_add_agent(self, temp_project):
        """Test add_agent method."""
        cm = ConfigManager(temp_project)
        cm.init_project_config("Test", force=True)
        
        cm.add_agent("Claude")
        agents = cm.get_agents()
        
        assert "Claude" in agents
    
    def test_remove_agent(self, temp_project):
        """Test remove_agent method."""
        cm = ConfigManager(temp_project)
        cm.init_project_config("Test", agents=["Claude", "Copilot"], force=True)
        
        removed = cm.remove_agent("Claude")
        agents = cm.get_agents()
        
        assert removed
        assert "Claude" not in agents
        assert "Copilot" in agents
    
    def test_get_agents(self, temp_project):
        """Test get_agents method."""
        cm = ConfigManager(temp_project)
        cm.init_project_config("Test", agents=["Claude", "Copilot"], force=True)
        
        agents = cm.get_agents()
        
        assert agents == ["Claude", "Copilot"]
