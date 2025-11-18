"""
Integration tests for Sprint 2 components.

Tests the complete sprint lifecycle and interaction between:
- FolderManager
- TemplateEngine
- MetadataManager
- SprintManager
"""
import shutil
import tempfile
from pathlib import Path
import pytest

from stride.core.folder_manager import FolderManager, SprintStatus
from stride.core.sprint_manager import SprintManager
from stride.core.template_engine import TemplateEngine
from stride.core.metadata_manager import MetadataManager


@pytest.fixture
def temp_project():
    """Create temporary project directory."""
    tmp = Path(tempfile.mkdtemp())
    yield tmp
    shutil.rmtree(tmp)


@pytest.fixture
def integrated_managers(temp_project):
    """Create integrated manager instances."""
    fm = FolderManager(temp_project)
    fm.ensure_structure()
    te = TemplateEngine()
    mm = MetadataManager()
    sm = SprintManager(folder_manager=fm, template_engine=te, metadata_manager=mm)
    return fm, te, mm, sm


class TestSprintLifecycle:
    """Test complete sprint lifecycle from proposal to completion."""
    
    def test_full_sprint_lifecycle(self, integrated_managers):
        """Test complete sprint lifecycle: proposed → active → review → completed."""
        fm, te, mm, sm = integrated_managers
        
        # Step 1: Create sprint in PROPOSED
        sprint_id = "SPRINT-LIFE"
        sprint_path = sm.create_sprint(
            sprint_id=sprint_id,
            title="Lifecycle Test Sprint",
            description="Testing full lifecycle",
            author="dev@example.com",
            tags=["test", "integration"],
            priority="high"
        )
        
        assert sprint_path.exists()
        assert (sprint_path / "proposal.md").exists()
        
        # Verify metadata
        meta = sm.get_sprint_metadata(sprint_id)
        assert meta["id"] == sprint_id
        assert meta["status"] == "proposed"
        assert meta["priority"] == "high"
        assert "test" in meta["tags"]
        
        # Step 2: Move to ACTIVE
        success = sm.move_sprint_status(sprint_id, SprintStatus.ACTIVE)
        assert success is True
        
        # Verify folder moved
        assert fm.get_sprint_path(sprint_id, SprintStatus.ACTIVE).exists()
        assert not fm.get_sprint_path(sprint_id, SprintStatus.PROPOSED).exists()
        
        # Verify metadata updated
        meta = sm.get_sprint_metadata(sprint_id)
        assert meta["status"] == "active"
        assert "updated" in meta
        
        # Step 3: Move to REVIEW
        success = sm.move_sprint_status(sprint_id, SprintStatus.REVIEW)
        assert success is True
        assert fm.get_sprint_path(sprint_id, SprintStatus.REVIEW).exists()
        
        meta = sm.get_sprint_metadata(sprint_id)
        assert meta["status"] == "review"
        
        # Step 4: Move to COMPLETED
        success = sm.move_sprint_status(sprint_id, SprintStatus.COMPLETED)
        assert success is True
        assert fm.get_sprint_path(sprint_id, SprintStatus.COMPLETED).exists()
        
        meta = sm.get_sprint_metadata(sprint_id)
        assert meta["status"] == "completed"
        
        # Verify sprint count
        assert fm.get_sprint_count(SprintStatus.COMPLETED) == 1
        assert fm.get_sprint_count() == 1
    
    def test_sprint_blocking_and_unblocking(self, integrated_managers):
        """Test blocking a sprint and moving it back to active."""
        fm, te, mm, sm = integrated_managers
        
        sprint_id = "SPRINT-BLOCK"
        sm.create_sprint(
            sprint_id=sprint_id,
            title="Block Test",
            description="Test blocking",
            author="dev@example.com"
        )
        
        # Move to active first
        sm.move_sprint_status(sprint_id, SprintStatus.ACTIVE)
        
        # Block with reason
        success = sm.move_sprint_status(
            sprint_id, 
            SprintStatus.BLOCKED, 
            reason="Waiting for API approval"
        )
        assert success is True
        
        # Verify blocked
        meta = sm.get_sprint_metadata(sprint_id)
        assert meta["status"] == "blocked"
        assert meta["reason"] == "Waiting for API approval"
        
        # Unblock back to active
        sm.update_sprint_metadata(sprint_id, {"reason": None})
        sm.move_sprint_status(sprint_id, SprintStatus.ACTIVE)
        
        meta = sm.get_sprint_metadata(sprint_id)
        assert meta["status"] == "active"
    
    def test_archive_and_restore_sprint(self, integrated_managers):
        """Test archiving and restoring a sprint."""
        fm, te, mm, sm = integrated_managers
        
        sprint_id = "SPRINT-ARCH"
        sm.create_sprint(
            sprint_id=sprint_id,
            title="Archive Test",
            description="Test archiving",
            author="dev@example.com"
        )
        
        # Archive from proposed
        archive_path = fm.archive_sprint(sprint_id, SprintStatus.PROPOSED)
        assert archive_path.exists()
        assert ".archive" in str(archive_path)
        assert not fm.get_sprint_path(sprint_id, SprintStatus.PROPOSED).exists()
        
        # Restore back to proposed
        restored_path = fm.restore_sprint(sprint_id, SprintStatus.PROPOSED)
        assert restored_path.exists()
        assert fm.sprint_exists(sprint_id, SprintStatus.PROPOSED)
        
        # Verify metadata intact
        meta = sm.get_sprint_metadata(sprint_id)
        assert meta["id"] == sprint_id
        assert meta["title"] == "Archive Test"


class TestMetadataOperations:
    """Test metadata operations across sprint lifecycle."""
    
    def test_metadata_updates_persist(self, integrated_managers):
        """Test that metadata updates persist across state transitions."""
        fm, te, mm, sm = integrated_managers
        
        sprint_id = "SPRINT-META"
        sm.create_sprint(
            sprint_id=sprint_id,
            title="Metadata Test",
            description="Test metadata",
            author="original@example.com"
        )
        
        # Update metadata
        sm.update_sprint_metadata(sprint_id, {
            "assignee": "alice@example.com",
            "estimated_hours": 8,
            "priority": "critical"
        })
        
        # Move to active
        sm.move_sprint_status(sprint_id, SprintStatus.ACTIVE)
        
        # Verify metadata persisted
        meta = sm.get_sprint_metadata(sprint_id)
        assert meta["assignee"] == "alice@example.com"
        assert meta["estimated_hours"] == 8
        assert meta["priority"] == "critical"
        assert meta["status"] == "active"
    
    def test_metadata_merge_vs_replace(self, integrated_managers):
        """Test merge vs replace modes for metadata updates."""
        fm, te, mm, sm = integrated_managers
        
        sprint_id = "SPRINT-MERGE"
        sm.create_sprint(
            sprint_id=sprint_id,
            title="Merge Test",
            description="Test merge",
            author="dev@example.com",
            tags=["original"],
            priority="low"
        )
        
        # Merge update (default)
        sm.update_sprint_metadata(sprint_id, {"assignee": "bob@example.com"}, merge=True)
        meta = sm.get_sprint_metadata(sprint_id)
        assert meta["assignee"] == "bob@example.com"
        assert meta["tags"] == ["original"]  # Original field preserved
        assert meta["priority"] == "low"  # Original field preserved
        
        # Replace update
        new_meta = {
            "id": sprint_id,
            "title": "Replaced Title",
            "status": "proposed",
            "created": meta["created"],  # Keep original created
            "updated": meta["updated"],
            "priority": "high"
        }
        sm.update_sprint_metadata(sprint_id, new_meta, merge=False)
        meta = sm.get_sprint_metadata(sprint_id)
        assert meta["title"] == "Replaced Title"
        assert meta["priority"] == "high"
        assert "assignee" not in meta  # Previous field removed
        assert "tags" not in meta  # Previous field removed


class TestTemplateRendering:
    """Test template rendering with real sprint data."""
    
    def test_proposal_rendering(self, integrated_managers):
        """Test that proposals are rendered correctly."""
        fm, te, mm, sm = integrated_managers
        
        sprint_id = "SPRINT-TMPL"
        sprint_path = sm.create_sprint(
            sprint_id=sprint_id,
            title="Template Test Sprint",
            description="This tests template rendering",
            author="template@example.com",
            tags=["template", "test"],
            priority="medium"
        )
        
        proposal_file = sprint_path / "proposal.md"
        content = proposal_file.read_text(encoding="utf-8")
        
        # Check frontmatter present
        assert content.startswith("---")
        
        # Check body rendered
        assert "Template Test Sprint" in content
        assert "This tests template rendering" in content
        
        # Parse and verify metadata
        meta, body = mm.parse_file(proposal_file)
        assert meta["id"] == sprint_id
        assert meta["title"] == "Template Test Sprint"
        assert meta["status"] == "proposed"
        assert meta["priority"] == "medium"
        assert "template" in meta["tags"]


class TestValidationAndErrorHandling:
    """Test validation and error handling."""
    
    def test_validate_sprint_structure(self, integrated_managers):
        """Test sprint validation."""
        fm, te, mm, sm = integrated_managers
        
        sprint_id = "SPRINT-VALID"
        sm.create_sprint(
            sprint_id=sprint_id,
            title="Valid Sprint",
            description="Valid",
            author="valid@example.com"
        )
        
        # Should be valid
        is_valid, errors = sm.validate_sprint(sprint_id)
        assert is_valid is True
        assert len(errors) == 0
        
        # Corrupt sprint by removing proposal
        sprint_path = fm.get_sprint_path(sprint_id, SprintStatus.PROPOSED)
        (sprint_path / "proposal.md").unlink()
        
        # Should be invalid
        is_valid, errors = sm.validate_sprint(sprint_id)
        assert is_valid is False
        assert len(errors) > 0
        assert any("proposal" in e.lower() for e in errors)
    
    def test_status_mismatch_detection(self, integrated_managers):
        """Test detection of status mismatch between folder and metadata."""
        fm, te, mm, sm = integrated_managers
        
        sprint_id = "SPRINT-MISM"
        sm.create_sprint(
            sprint_id=sprint_id,
            title="Mismatch Test",
            description="Test mismatch",
            author="dev@example.com"
        )
        
        # Manually corrupt: move folder but don't update metadata
        source = fm.get_sprint_path(sprint_id, SprintStatus.PROPOSED)
        dest = fm.get_sprint_path(sprint_id, SprintStatus.ACTIVE)
        source.rename(dest)
        
        # Validation should detect mismatch
        is_valid, errors = sm.validate_sprint(sprint_id)
        assert is_valid is False
        assert any("mismatch" in e.lower() for e in errors)
    
    def test_move_nonexistent_sprint(self, integrated_managers):
        """Test moving a sprint that doesn't exist."""
        fm, te, mm, sm = integrated_managers
        
        success = sm.move_sprint_status("SPRINT-NOEXIST", SprintStatus.ACTIVE)
        assert success is False
    
    def test_get_metadata_nonexistent_sprint(self, integrated_managers):
        """Test getting metadata for nonexistent sprint."""
        fm, te, mm, sm = integrated_managers
        
        meta = sm.get_sprint_metadata("SPRINT-NOEXIST")
        assert meta is None


class TestMultiSprintOperations:
    """Test operations with multiple sprints."""
    
    def test_list_all_sprints_multiple_statuses(self, integrated_managers):
        """Test listing sprints across multiple statuses."""
        fm, te, mm, sm = integrated_managers
        
        # Create sprints in different statuses
        sprints = [
            ("SPRINT-A1", SprintStatus.PROPOSED),
            ("SPRINT-A2", SprintStatus.PROPOSED),
            ("SPRINT-B1", SprintStatus.ACTIVE),
            ("SPRINT-C1", SprintStatus.REVIEW),
            ("SPRINT-D1", SprintStatus.COMPLETED),
            ("SPRINT-D2", SprintStatus.COMPLETED),
        ]
        
        for sprint_id, status in sprints:
            sm.create_sprint(
                sprint_id=sprint_id,
                title=f"Sprint {sprint_id}",
                description=f"Test sprint {sprint_id}",
                author="dev@example.com"
            )
            if status != SprintStatus.PROPOSED:
                sm.move_sprint_status(sprint_id, status)
        
        # List all sprints
        all_sprints = sm.list_all_sprints()
        assert len(all_sprints) == 6
        
        # Verify statuses
        sprint_dict = {s["id"]: s["status"] for s in all_sprints}
        assert sprint_dict["SPRINT-A1"] == SprintStatus.PROPOSED
        assert sprint_dict["SPRINT-B1"] == SprintStatus.ACTIVE
        assert sprint_dict["SPRINT-C1"] == SprintStatus.REVIEW
        assert sprint_dict["SPRINT-D1"] == SprintStatus.COMPLETED
        
        # Verify counts
        assert fm.get_sprint_count(SprintStatus.PROPOSED) == 2
        assert fm.get_sprint_count(SprintStatus.ACTIVE) == 1
        assert fm.get_sprint_count(SprintStatus.REVIEW) == 1
        assert fm.get_sprint_count(SprintStatus.COMPLETED) == 2
        assert fm.get_sprint_count() == 6
    
    def test_get_sprint_with_full_info(self, integrated_managers):
        """Test get_sprint returns complete information."""
        fm, te, mm, sm = integrated_managers
        
        sprint_id = "SPRINT-FULL"
        sm.create_sprint(
            sprint_id=sprint_id,
            title="Full Info Sprint",
            description="Test full info",
            author="dev@example.com",
            tags=["full", "info"],
            priority="high"
        )
        
        # Get full sprint info
        sprint_info = sm.get_sprint(sprint_id)
        
        assert sprint_info is not None
        assert sprint_info["id"] == sprint_id
        assert sprint_info["status"] == SprintStatus.PROPOSED
        assert isinstance(sprint_info["path"], Path)
        assert sprint_info["path"].exists()
        
        meta = sprint_info["metadata"]
        assert meta["title"] == "Full Info Sprint"
        assert meta["priority"] == "high"
        assert "full" in meta["tags"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
