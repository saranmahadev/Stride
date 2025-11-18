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
    
    def test_validate_structure(self, temp_project):
        """Test structure validation."""
        fm = FolderManager(temp_project)
        
        # Before creating structure
        results = fm.validate_structure()
        assert not all(results.values())
        
        # After creating structure
        fm.ensure_structure()
        results = fm.validate_structure()
        assert all(results.values())
        assert results["stride_root"] is True
        assert results["sprints_root"] is True
    
    def test_list_sprints_by_status(self, temp_project):
        """Test listing sprints by status."""
        fm = FolderManager(temp_project)
        fm.ensure_structure()
        
        # Create test sprints
        fm.create_sprint_folder("SPRINT-AAA1", SprintStatus.PROPOSED)
        fm.create_sprint_folder("SPRINT-BBB2", SprintStatus.PROPOSED)
        fm.create_sprint_folder("SPRINT-CCC3", SprintStatus.ACTIVE)
        
        # List proposed sprints
        proposed = fm.list_sprints_by_status(SprintStatus.PROPOSED)
        assert len(proposed) == 2
        assert "SPRINT-AAA1" in proposed
        assert "SPRINT-BBB2" in proposed
        
        # List active sprints
        active = fm.list_sprints_by_status(SprintStatus.ACTIVE)
        assert len(active) == 1
        assert "SPRINT-CCC3" in active
    
    def test_move_sprint(self, temp_project):
        """Test moving sprint between statuses."""
        fm = FolderManager(temp_project)
        fm.ensure_structure()
        
        # Create sprint in proposed
        fm.create_sprint_folder("SPRINT-MOVE", SprintStatus.PROPOSED)
        
        # Move to active
        new_path = fm.move_sprint("SPRINT-MOVE", SprintStatus.PROPOSED, SprintStatus.ACTIVE)
        assert new_path.exists()
        assert new_path.parent.name == "active"
        assert not fm.get_sprint_path("SPRINT-MOVE", SprintStatus.PROPOSED).exists()
    
    def test_move_sprint_not_found(self, temp_project):
        """Test moving non-existent sprint raises error."""
        fm = FolderManager(temp_project)
        fm.ensure_structure()
        
        with pytest.raises(FileNotFoundError):
            fm.move_sprint("SPRINT-NOTFOUND", SprintStatus.PROPOSED, SprintStatus.ACTIVE)
    
    def test_archive_sprint(self, temp_project):
        """Test archiving a sprint."""
        fm = FolderManager(temp_project)
        fm.ensure_structure()
        
        # Create and archive sprint
        fm.create_sprint_folder("SPRINT-ARCH", SprintStatus.ACTIVE)
        archive_path = fm.archive_sprint("SPRINT-ARCH", SprintStatus.ACTIVE)
        
        assert archive_path.exists()
        assert ".archive" in str(archive_path)
        assert not fm.get_sprint_path("SPRINT-ARCH", SprintStatus.ACTIVE).exists()
    
    def test_archive_sprint_not_found(self, temp_project):
        """Test archiving non-existent sprint raises error."""
        fm = FolderManager(temp_project)
        fm.ensure_structure()
        
        with pytest.raises(FileNotFoundError):
            fm.archive_sprint("SPRINT-NOTFOUND", SprintStatus.ACTIVE)
    
    def test_restore_sprint(self, temp_project):
        """Test restoring a sprint from archive."""
        fm = FolderManager(temp_project)
        fm.ensure_structure()
        
        # Create, archive, then restore sprint
        fm.create_sprint_folder("SPRINT-RESTORE", SprintStatus.COMPLETED)
        fm.archive_sprint("SPRINT-RESTORE", SprintStatus.COMPLETED)
        
        restored_path = fm.restore_sprint("SPRINT-RESTORE", SprintStatus.COMPLETED)
        
        assert restored_path.exists()
        assert restored_path.parent.name == "completed"
        assert fm.sprint_exists("SPRINT-RESTORE", SprintStatus.COMPLETED)
    
    def test_delete_sprint(self, temp_project):
        """Test hard deleting a sprint."""
        fm = FolderManager(temp_project)
        fm.ensure_structure()
        
        # Create and delete sprint
        fm.create_sprint_folder("SPRINT-DEL", SprintStatus.REVIEW)
        result = fm.delete_sprint("SPRINT-DEL", SprintStatus.REVIEW)
        
        assert result is True
        assert not fm.sprint_exists("SPRINT-DEL", SprintStatus.REVIEW)
    
    def test_delete_sprint_not_found(self, temp_project):
        """Test deleting non-existent sprint returns False."""
        fm = FolderManager(temp_project)
        fm.ensure_structure()
        
        result = fm.delete_sprint("SPRINT-NOTFOUND", SprintStatus.REVIEW)
        assert result is False
    
    def test_get_sprint_count(self, temp_project):
        """Test counting sprints."""
        fm = FolderManager(temp_project)
        fm.ensure_structure()
        
        # Initially zero
        assert fm.get_sprint_count() == 0
        assert fm.get_sprint_count(SprintStatus.PROPOSED) == 0
        
        # Add some sprints
        fm.create_sprint_folder("SPRINT-1", SprintStatus.PROPOSED)
        fm.create_sprint_folder("SPRINT-2", SprintStatus.PROPOSED)
        fm.create_sprint_folder("SPRINT-3", SprintStatus.ACTIVE)
        
        assert fm.get_sprint_count() == 3
        assert fm.get_sprint_count(SprintStatus.PROPOSED) == 2
        assert fm.get_sprint_count(SprintStatus.ACTIVE) == 1
    
    def test_get_all_sprints_with_status(self, temp_project):
        """Test getting all sprints organized by status."""
        fm = FolderManager(temp_project)
        fm.ensure_structure()
        
        # Create sprints in different statuses
        fm.create_sprint_folder("SPRINT-P1", SprintStatus.PROPOSED)
        fm.create_sprint_folder("SPRINT-A1", SprintStatus.ACTIVE)
        fm.create_sprint_folder("SPRINT-A2", SprintStatus.ACTIVE)
        
        all_sprints = fm.get_all_sprints_with_status()
        
        assert len(all_sprints[SprintStatus.PROPOSED]) == 1
        assert len(all_sprints[SprintStatus.ACTIVE]) == 2
        assert len(all_sprints[SprintStatus.BLOCKED]) == 0
        assert "SPRINT-P1" in all_sprints[SprintStatus.PROPOSED]
        assert "SPRINT-A1" in all_sprints[SprintStatus.ACTIVE]


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
