"""
Basic tests for Stride core functionality.
"""
import pytest
from pathlib import Path
import tempfile
import shutil

from stride.core.folder_manager import FolderManager, SprintStatus
from stride.core.sprint_manager import SprintManager
from stride.core.config_manager import ConfigManager
from stride.utils.id_generator import generate_sprint_id, validate_sprint_id


class TestFolderManager:
    """Tests for FolderManager class."""
    
    @pytest.fixture
    def temp_project(self):
        """Create a temporary project directory."""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    def test_folder_manager_init(self, temp_project):
        """Test FolderManager initialization."""
        fm = FolderManager(temp_project)
        assert fm.project_root == temp_project
        assert fm.stride_root == temp_project / "stride"
    
    def test_ensure_structure(self, temp_project):
        """Test creation of directory structure."""
        fm = FolderManager(temp_project)
        fm.ensure_structure()
        
        assert (temp_project / "stride").exists()
        assert (temp_project / "stride" / "sprints").exists()
        assert (temp_project / "stride" / "sprints" / "proposed").exists()
        assert (temp_project / "stride" / "sprints" / "active").exists()
        assert (temp_project / "stride" / "sprints" / "completed").exists()
    
    def test_create_sprint_folder(self, temp_project):
        """Test sprint folder creation."""
        fm = FolderManager(temp_project)
        fm.ensure_structure()
        
        sprint_id = "SPRINT-TEST"
        path = fm.create_sprint_folder(sprint_id, SprintStatus.PROPOSED)
        
        assert path.exists()
        assert path.name == sprint_id


class TestSprintManager:
    """Tests for SprintManager class."""
    
    @pytest.fixture
    def temp_project(self):
        """Create a temporary project directory."""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    def test_sprint_manager_init(self, temp_project):
        """Test SprintManager initialization."""
        fm = FolderManager(temp_project)
        sm = SprintManager(fm)
        assert sm.folder_manager == fm
    
    def test_create_sprint(self, temp_project):
        """Test sprint creation with metadata."""
        fm = FolderManager(temp_project)
        fm.ensure_structure()
        sm = SprintManager(fm)
        
        sprint_id = "SPRINT-TEST"
        path = sm.create_sprint(
            sprint_id=sprint_id,
            title="Test Sprint",
            description="Test description",
            author="test@example.com",
            status=SprintStatus.PROPOSED
        )
        
        assert path.exists()
        assert (path / "proposal.md").exists()


class TestConfigManager:
    """Tests for ConfigManager class."""
    
    @pytest.fixture
    def temp_project(self):
        """Create a temporary project directory."""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    def test_config_manager_init(self, temp_project):
        """Test ConfigManager initialization."""
        cm = ConfigManager(temp_project)
        assert cm.project_root == temp_project
    
    def test_init_project_config(self, temp_project):
        """Test project configuration initialization."""
        cm = ConfigManager(temp_project)
        cm.init_project_config("Test Project", ["Claude Code"])
        
        config = cm.get_project_config()
        assert config["project"]["name"] == "Test Project"
        assert "Claude Code" in config["project"]["agents"]


class TestIDGenerator:
    """Tests for ID generation utilities."""
    
    def test_generate_sprint_id(self):
        """Test sprint ID generation."""
        sprint_id = generate_sprint_id()
        assert sprint_id.startswith("SPRINT-")
        assert len(sprint_id) == 11  # SPRINT- + 4 chars
    
    def test_generate_unique_ids(self):
        """Test that generated IDs are unique."""
        ids = {generate_sprint_id() for _ in range(100)}
        assert len(ids) == 100  # All unique
    
    def test_validate_sprint_id(self):
        """Test sprint ID validation."""
        assert validate_sprint_id("SPRINT-A2B3")
        assert validate_sprint_id("SPRINT-TEST")
        assert not validate_sprint_id("INVALID")
        assert not validate_sprint_id("SPRINT-")
        assert not validate_sprint_id("sprint-test")  # lowercase


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
