"""
Tests for the Stride CLI commands.
"""
import shutil
import tempfile
from pathlib import Path
import pytest
from click.testing import CliRunner

from stride.cli.main import cli
from stride.core.folder_manager import FolderManager, SprintStatus
from stride.core.sprint_manager import SprintManager


@pytest.fixture
def temp_project():
    """Create temporary project directory."""
    tmp = Path(tempfile.mkdtemp())
    yield tmp
    shutil.rmtree(tmp)


@pytest.fixture
def runner():
    """Create Click CLI runner."""
    return CliRunner()


def make_context(temp_project: Path) -> dict:
    """Create CLI context with managers for temp project."""
    fm = FolderManager(temp_project)
    sm = SprintManager(fm)
    return {
        "project_root": temp_project,
        "folder_manager": fm,
        "sprint_manager": sm,
        "verbose": False,
        "quiet": False
    }


class TestCLIBasics:
    """Test basic CLI functionality."""
    
    def test_cli_help(self, runner):
        """Test CLI help command."""
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Stride - Sprint-Powered" in result.output
        assert "stride init" in result.output
        assert "stride create" in result.output
    
    def test_cli_version(self, runner):
        """Test CLI version command."""
        result = runner.invoke(cli, ["version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output
        assert "Stride" in result.output
    
    def test_cli_version_flag(self, runner):
        """Test --version flag."""
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output


class TestInitCommand:
    """Test stride init command."""
    
    def test_init_creates_structure(self, runner):
        """Test that init creates Stride folder structure."""
        with runner.isolated_filesystem() as temp_dir:
            temp_project = Path(temp_dir)
            result = runner.invoke(cli, ["init", "--no-interactive"], obj=make_context(temp_project))
            
            assert result.exit_code == 0
            assert "✓" in result.output or "initialized" in result.output.lower()
            
            # Verify structure created
            assert (temp_project / "stride").exists()
            assert (temp_project / "stride" / "sprints" / "proposed").exists()
            assert (temp_project / "stride" / "sprints" / "active").exists()
            assert (temp_project / "stride" / "sprints" / "completed").exists()
    
    def test_init_already_initialized(self, runner):
        """Test init fails when already initialized."""
        with runner.isolated_filesystem() as temp_dir:
            temp_project = Path(temp_dir)
            # First init
            result1 = runner.invoke(cli, ["init", "--no-interactive"], obj=make_context(temp_project))
            assert result1.exit_code == 0
            
            # Second init without force
            result2 = runner.invoke(cli, ["init", "--no-interactive"], obj=make_context(temp_project))
            assert result2.exit_code == 1
            assert "already initialized" in result2.output.lower()
    
    def test_init_force_reinitialize(self, runner):
        """Test init --force reinitializes."""
        with runner.isolated_filesystem() as temp_dir:
            temp_project = Path(temp_dir)
            # First init
            result1 = runner.invoke(cli, ["init", "--no-interactive"], obj=make_context(temp_project))
            assert result1.exit_code == 0
            
            # Second init with force
            result2 = runner.invoke(cli, ["init", "--force", "--no-interactive"], obj=make_context(temp_project))
            assert result2.exit_code == 0


class TestCreateCommand:
    """Test stride create command."""
    
    def test_create_with_title_only(self, runner, temp_project):
        """Test creating sprint with just title."""
        runner.invoke(cli, ["init"], obj=make_context(temp_project))
        
        result = runner.invoke(
            cli, 
            ["create", "--title", "Test Sprint"],
            obj=make_context(temp_project)
        )
        
        assert result.exit_code == 0
        assert "✓" in result.output or "created" in result.output.lower()
        assert "SPRINT-" in result.output
    
    def test_create_with_custom_id(self, runner, temp_project):
        """Test creating sprint with custom ID."""
        runner.invoke(cli, ["init"], obj=make_context(temp_project))
        
        result = runner.invoke(
            cli,
            ["create", "--id", "SPRINT-TEST", "--title", "Custom ID Sprint"],
            obj=make_context(temp_project)
        )
        
        assert result.exit_code == 0
        assert "SPRINT-TEST" in result.output
    
    def test_create_with_all_options(self, runner, temp_project):
        """Test creating sprint with all options."""
        runner.invoke(cli, ["init"], obj=make_context(temp_project))
        
        result = runner.invoke(
            cli,
            [
                "create",
                "--title", "Full Options Sprint",
                "--description", "A sprint with all options",
                "--author", "test@example.com",
                "--priority", "high",
                "--tags", "test,cli,full"
            ],
            obj=make_context(temp_project)
        )
        
        assert result.exit_code == 0
        assert "high" in result.output
    
    def test_create_missing_title(self, runner, temp_project):
        """Test create fails without title."""
        runner.invoke(cli, ["init"], obj=make_context(temp_project))
        
        result = runner.invoke(cli, ["create"], obj=make_context(temp_project))
        
        assert result.exit_code != 0
    
    def test_create_invalid_sprint_id(self, runner, temp_project):
        """Test create fails with invalid sprint ID format."""
        runner.invoke(cli, ["init"], obj=make_context(temp_project))
        
        result = runner.invoke(
            cli,
            ["create", "--id", "invalid-id", "--title", "Test"],
            obj=make_context(temp_project)
        )
        
        assert result.exit_code == 1
        assert "invalid" in result.output.lower()


class TestListCommand:
    """Test stride list command."""
    
    def test_list_empty(self, runner, temp_project):
        """Test list with no sprints."""
        runner.invoke(cli, ["init"], obj=make_context(temp_project))
        
        result = runner.invoke(cli, ["list"], obj=make_context(temp_project))
        
        assert result.exit_code == 0
        assert "no sprints" in result.output.lower() or len(result.output.strip()) == 0
    
    def test_list_with_sprints(self, runner, temp_project):
        """Test list shows created sprints."""
        runner.invoke(cli, ["init"], obj=make_context(temp_project))
        runner.invoke(
            cli,
            ["create", "--id", "SPRINT-LST1", "--title", "Sprint 1"],
            obj=make_context(temp_project)
        )
        runner.invoke(
            cli,
            ["create", "--id", "SPRINT-LST2", "--title", "Sprint 2"],
            obj=make_context(temp_project)
        )
        
        result = runner.invoke(cli, ["list", "--format", "table"], obj=make_context(temp_project))
        
        assert result.exit_code == 0
        assert "SPRINT-LST1" in result.output
        assert "SPRINT-LST2" in result.output
    
    def test_list_filter_by_status(self, runner):
        """Test list filtering by status."""
        with runner.isolated_filesystem() as temp_dir:
            temp_project = Path(temp_dir)
            ctx = make_context(temp_project)
            
            result1 = runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
            assert result1.exit_code == 0, f"Init failed: {result1.output}"
            
            result2 = runner.invoke(
                cli,
                ["create", "--id", "SPRINT-ACT1", "--title", "Active Sprint"],
                obj=ctx
            )
            assert result2.exit_code == 0, f"Create failed: {result2.output}"
            
            result3 = runner.invoke(
                cli,
                ["move", "SPRINT-ACT1", "active"],
                obj=ctx
            )
            assert result3.exit_code == 0, f"Move failed: {result3.output}"
            
            result = runner.invoke(
                cli,
                ["list", "--status", "active", "--format", "table"],
                obj=ctx
            )
            
            assert result.exit_code == 0
            assert "SPRINT-ACT1" in result.output
    
    def test_list_json_format(self, runner, temp_project):
        """Test list with JSON format."""
        runner.invoke(cli, ["init"], obj=make_context(temp_project))
        runner.invoke(
            cli,
            ["create", "--id", "SPRINT-JSON", "--title", "JSON Sprint"],
            obj=make_context(temp_project)
        )
        
        result = runner.invoke(
            cli,
            ["list", "--format", "json"],
            obj=make_context(temp_project)
        )
        
        assert result.exit_code == 0
        assert "SPRINT-JSON" in result.output
        assert "[" in result.output  # JSON array


class TestStatusCommand:
    """Test stride status command."""
    
    def test_status_existing_sprint(self, runner, temp_project):
        """Test status shows sprint details."""
        runner.invoke(cli, ["init"], obj=make_context(temp_project))
        runner.invoke(
            cli,
            ["create", "--id", "SPRINT-STAT", "--title", "Status Test"],
            obj=make_context(temp_project)
        )
        
        result = runner.invoke(
            cli,
            ["status", "SPRINT-STAT"],
            obj=make_context(temp_project)
        )
        
        assert result.exit_code == 0
        assert "SPRINT-STAT" in result.output
        assert "Status Test" in result.output
        assert "proposed" in result.output.lower()
    
    def test_status_nonexistent_sprint(self, runner, temp_project):
        """Test status fails for nonexistent sprint."""
        runner.invoke(cli, ["init"], obj=make_context(temp_project))
        
        result = runner.invoke(
            cli,
            ["status", "SPRINT-NOEXIST"],
            obj=make_context(temp_project)
        )
        
        assert result.exit_code == 1
        assert "not found" in result.output.lower()


class TestMoveCommand:
    """Test stride move command."""
    
    def test_move_to_active(self, runner, temp_project):
        """Test moving sprint to active status."""
        runner.invoke(cli, ["init"], obj=make_context(temp_project))
        create_result = runner.invoke(
            cli,
            ["create", "--id", "SPRINT-MOVE", "--title", "Move Test", "--author", "test@example.com"],
            obj=make_context(temp_project)
        )
        assert create_result.exit_code == 0, f"Create failed: {create_result.output}"
        
        result = runner.invoke(
            cli,
            ["move", "SPRINT-MOVE", "active"],
            obj=make_context(temp_project)
        )
        
        assert result.exit_code == 0
        assert "✓" in result.output or "moved" in result.output.lower()
        assert "active" in result.output.lower()
        
        # Verify sprint moved
        fm = FolderManager(temp_project)
        assert fm.get_sprint_path("SPRINT-MOVE", SprintStatus.ACTIVE).exists()
    
    def test_move_with_reason(self, runner, temp_project):
        """Test moving sprint with reason."""
        runner.invoke(cli, ["init"], obj=make_context(temp_project))
        runner.invoke(
            cli,
            ["create", "--id", "SPRINT-BLCK", "--title", "Block Test", "--author", "test@example.com"],
            obj=make_context(temp_project)
        )
        
        result = runner.invoke(
            cli,
            ["move", "SPRINT-BLCK", "blocked", "--reason", "Waiting for approval"],
            obj=make_context(temp_project)
        )
        
        assert result.exit_code == 0
        assert "approval" in result.output
    
    def test_move_nonexistent_sprint(self, runner, temp_project):
        """Test move fails for nonexistent sprint."""
        runner.invoke(cli, ["init"], obj=make_context(temp_project))
        
        result = runner.invoke(
            cli,
            ["move", "SPRINT-NOEXIST", "active"],
            obj=make_context(temp_project)
        )
        
        assert result.exit_code == 1


class TestValidateCommand:
    """Test stride validate command."""
    
    def test_validate_single_sprint(self, runner, temp_project):
        """Test validating a single sprint."""
        runner.invoke(cli, ["init"], obj=make_context(temp_project))
        runner.invoke(
            cli,
            ["create", "--id", "SPRINT-VALD", "--title", "Valid Sprint"],
            obj=make_context(temp_project)
        )
        
        result = runner.invoke(
            cli,
            ["validate", "SPRINT-VALD"],
            obj=make_context(temp_project)
        )
        
        assert result.exit_code == 0
        assert "✓" in result.output or "valid" in result.output.lower()
    
    def test_validate_all(self, runner, temp_project):
        """Test validating all sprints."""
        ctx = make_context(temp_project)
        runner.invoke(cli, ["init"], obj=ctx)
        runner.invoke(
            cli,
            ["create", "--id", "SPRINT-VAL1", "--title", "Sprint 1"],
            obj=ctx
        )
        runner.invoke(
            cli,
            ["create", "--id", "SPRINT-VAL2", "--title", "Sprint 2"],
            obj=ctx
        )
        
        result = runner.invoke(
            cli,
            ["validate", "--all"],
            obj=ctx
        )
        
        assert result.exit_code == 0
        assert "SPRINT-VAL1" in result.output
        assert "SPRINT-VAL2" in result.output


class TestArchiveCommand:
    """Test stride archive command."""
    
    def test_archive_single_sprint(self, runner, temp_project):
        """Test archiving a single sprint."""
        runner.invoke(cli, ["init"], obj=make_context(temp_project))
        runner.invoke(
            cli,
            ["create", "--id", "SPRINT-ARCH", "--title", "Archive Test"],
            obj=make_context(temp_project)
        )
        
        result = runner.invoke(
            cli,
            ["archive", "SPRINT-ARCH", "--yes"],
            obj=make_context(temp_project)
        )
        
        assert result.exit_code == 0
        assert "✓" in result.output or "archived" in result.output.lower()
        
        # Verify archived
        assert (temp_project / "stride" / "sprints" / ".archive").exists()
    
    def test_archive_without_confirmation(self, runner, temp_project):
        """Test archive requires confirmation without --yes."""
        runner.invoke(cli, ["init"], obj=make_context(temp_project))
        runner.invoke(
            cli,
            ["create", "--id", "SPRINT-CONF", "--title", "Confirm Test"],
            obj=make_context(temp_project)
        )
        
        # Without --yes, provide 'n' to confirmation
        result = runner.invoke(
            cli,
            ["archive", "SPRINT-CONF"],
            input="n\n",
            obj=make_context(temp_project)
        )
        
        assert "cancelled" in result.output.lower() or "abort" in result.output.lower()


class TestRestoreCommand:
    """Test stride restore command."""
    
    def test_restore_archived_sprint(self, runner, temp_project):
        """Test restoring an archived sprint."""
        runner.invoke(cli, ["init"], obj=make_context(temp_project))
        runner.invoke(
            cli,
            ["create", "--id", "SPRINT-REST", "--title", "Restore Test"],
            obj=make_context(temp_project)
        )
        runner.invoke(
            cli,
            ["archive", "SPRINT-REST", "--yes"],
            obj=make_context(temp_project)
        )
        
        result = runner.invoke(
            cli,
            ["restore", "SPRINT-REST", "proposed"],
            obj=make_context(temp_project)
        )
        
        assert result.exit_code == 0
        assert "✓" in result.output or "restored" in result.output.lower()
        
        # Verify restored
        fm = FolderManager(temp_project)
        assert fm.get_sprint_path("SPRINT-REST", SprintStatus.PROPOSED).exists()


class TestTimelineCommand:
    """Test stride timeline command for Sprint 12."""
    
    def test_timeline_displays_creation_event(self, runner, temp_project):
        """Test timeline command shows sprint creation event."""
        ctx = make_context(temp_project)

        # Setup
        runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
        runner.invoke(
            cli,
            ["create", "--id", "SPRINT-TL1X", "--title", "Timeline Test", "--author", "test@example.com"],
            obj=ctx
        )
        
        # Act
        result = runner.invoke(cli, ["timeline", "SPRINT-TL1X"], obj=ctx)
        
        # Assert
        assert result.exit_code == 0
        assert "SPRINT-TL1X" in result.output
        assert "created" in result.output.lower() or "Created" in result.output
        assert "test@example.com" in result.output
    
    def test_timeline_tracks_status_changes(self, runner, temp_project):
        """Test timeline command tracks status change events."""
        ctx = make_context(temp_project)
        
        # Setup
        runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
        runner.invoke(
            cli,
            ["create", "--id", "SPRINT-TL2X", "--title", "Status Change Test", "--author", "test@example.com"],
            obj=ctx
        )
        
        # Move sprint through statuses
        runner.invoke(cli, ["move", "SPRINT-TL2X", "active"], obj=ctx)
        runner.invoke(cli, ["move", "SPRINT-TL2X", "review"], obj=ctx)
        
        # Act
        result = runner.invoke(cli, ["timeline", "SPRINT-TL2X"], obj=ctx)
        
        # Assert
        assert result.exit_code == 0
        assert "status" in result.output.lower() or "Status" in result.output
        assert "proposed" in result.output.lower() or "active" in result.output.lower()
    
    def test_timeline_with_limit(self, runner, temp_project):
        """Test timeline command with --limit option."""
        ctx = make_context(temp_project)
        
        # Setup
        runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
        runner.invoke(
            cli,
            ["create", "--id", "SPRINT-TL3X", "--title", "Limit Test", "--author", "test@example.com"],
            obj=ctx
        )
        
        # Generate multiple events
        runner.invoke(cli, ["move", "SPRINT-TL3X", "active"], obj=ctx)
        runner.invoke(cli, ["move", "SPRINT-TL3X", "blocked", "--reason", "Test"], obj=ctx)
        runner.invoke(cli, ["move", "SPRINT-TL3X", "active"], obj=ctx)
        
        # Act - limit to 2 events
        result = runner.invoke(cli, ["timeline", "SPRINT-TL3X", "--limit", "2"], obj=ctx)
        
        # Assert
        assert result.exit_code == 0
        # Should show limited events
        assert "SPRINT-TL3X" in result.output
    
    def test_timeline_with_blocked_reason(self, runner, temp_project):
        """Test timeline command shows blocking reason."""
        ctx = make_context(temp_project)
        
        # Setup
        runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
        runner.invoke(
            cli,
            ["create", "--id", "SPRINT-TL4X", "--title", "Block Test", "--author", "test@example.com"],
            obj=ctx
        )
        
        # Block with reason
        runner.invoke(cli, ["move", "SPRINT-TL4X", "blocked", "--reason", "Waiting for API"], obj=ctx)
        
        # Act
        result = runner.invoke(cli, ["timeline", "SPRINT-TL4X"], obj=ctx)
        
        # Assert
        assert result.exit_code == 0
        assert "Waiting for API" in result.output or "blocked" in result.output.lower()
    
    def test_timeline_invalid_sprint(self, runner, temp_project):
        """Test timeline command with non-existent sprint."""
        ctx = make_context(temp_project)
        
        # Setup
        runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
        
        # Act
        result = runner.invoke(cli, ["timeline", "SPRINT-NONE"], obj=ctx)
        
        # Assert
        assert result.exit_code != 0
        assert "not found" in result.output.lower() or "error" in result.output.lower()
    
    def test_timeline_shows_event_count(self, runner, temp_project):
        """Test timeline command displays total event count."""
        ctx = make_context(temp_project)
        
        # Setup
        runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
        runner.invoke(
            cli,
            ["create", "--id", "SPRINT-TL5X", "--title", "Count Test", "--author", "test@example.com"],
            obj=ctx
        )
        
        # Act
        result = runner.invoke(cli, ["timeline", "SPRINT-TL5X"], obj=ctx)
        
        # Assert
        assert result.exit_code == 0
        assert "event" in result.output.lower() or "Event" in result.output
        # Should show at least the creation event
        assert "1" in result.output or "created" in result.output.lower()
    
    def test_timeline_empty_events(self, runner, temp_project):
        """Test timeline command with sprint that has no events (legacy sprint)."""
        ctx = make_context(temp_project)
        
        # Setup - create sprint manually without events
        runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
        
        # Create a sprint using the old method (before event tracking)
        from pathlib import Path
        fm = FolderManager(temp_project)
        sm = SprintManager(fm)
        
        # Create sprint folder
        sprint_path = fm.create_sprint_folder("SPRINT-TL6X", SprintStatus.PROPOSED)
        
        # Write minimal metadata without events
        proposal_file = sprint_path / "proposal.md"
        proposal_file.write_text("""---
id: SPRINT-TL6X
title: Legacy Sprint
status: proposed
created: 2025-11-19T00:00:00Z
author: test@example.com
---

# Legacy Sprint
No events tracked.""", encoding="utf-8")
        
        # Act
        result = runner.invoke(cli, ["timeline", "SPRINT-TL6X"], obj=ctx)
        
        # Assert
        assert result.exit_code == 0
        assert "No events" in result.output or "0" in result.output


class TestProgressCommand:
    """Test stride progress command for Sprint 11."""
    
    def test_progress_displays_metadata(self, runner, temp_project):
        """Test progress command displays sprint metadata."""
        ctx = make_context(temp_project)
        
        # Setup
        runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
        runner.invoke(
            cli,
            ["create", "--id", "SPRINT-PROG1", "--title", "Progress Test", "--author", "test@example.com"],
            obj=ctx
        )
        
        # Act
        result = runner.invoke(cli, ["progress", "SPRINT-PROG1"], obj=ctx)
        
        # Assert
        assert result.exit_code == 0
        assert "SPRINT-PROG1" in result.output
        assert "Progress Test" in result.output
        assert "test@example.com" in result.output
    
    def test_progress_no_tasks(self, runner, temp_project):
        """Test progress command with no tasks in plan.md."""
        ctx = make_context(temp_project)
        
        # Setup
        runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
        runner.invoke(
            cli,
            ["create", "--id", "SPRINT-PROG2", "--title", "No Tasks", "--author", "test@example.com"],
            obj=ctx
        )
        
        # Act
        result = runner.invoke(cli, ["progress", "SPRINT-PROG2"], obj=ctx)
        
        # Assert
        assert result.exit_code == 0
        assert "No tasks found" in result.output or "0 / 0" in result.output
    
    def test_progress_with_completed_tasks(self, runner, temp_project):
        """Test progress command calculates completion correctly."""
        ctx = make_context(temp_project)
        
        # Setup
        runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
        runner.invoke(
            cli,
            ["create", "--id", "SPRINT-PROG3", "--title", "Tasks Test", "--author", "test@example.com"],
            obj=ctx)
        
        # Add plan.md with tasks
        from pathlib import Path
        sprint_path = temp_project / "stride" / "sprints" / "proposed" / "SPRINT-PROG3"
        plan_file = sprint_path / "plan.md"
        plan_file.write_text("""---
id: SPRINT-PROG3
---

# Tasks

- [x] Completed task 1
- [x] Completed task 2
- [ ] Incomplete task 3
- [ ] Incomplete task 4
""", encoding="utf-8")
        
        # Act
        result = runner.invoke(cli, ["progress", "SPRINT-PROG3"], obj=ctx)
        
        # Assert
        assert result.exit_code == 0
        assert "2 / 4" in result.output or "50" in result.output  # 50% completion
    
    def test_progress_all_tasks_completed(self, runner, temp_project):
        """Test progress command with 100% completion."""
        ctx = make_context(temp_project)
        
        # Setup
        runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
        runner.invoke(
            cli,
            ["create", "--id", "SPRINT-PROG4", "--title", "All Done", "--author", "test@example.com"],
            obj=ctx
        )
        
        # Add plan.md with all completed tasks
        from pathlib import Path
        sprint_path = temp_project / "stride" / "sprints" / "proposed" / "SPRINT-PROG4"
        plan_file = sprint_path / "plan.md"
        plan_file.write_text("""---
id: SPRINT-PROG4
---

# Tasks

- [x] Task 1
- [x] Task 2
- [x] Task 3
""", encoding="utf-8")
        
        # Act
        result = runner.invoke(cli, ["progress", "SPRINT-PROG4"], obj=ctx)
        
        # Assert
        assert result.exit_code == 0
        assert "3 / 3" in result.output
        assert "100" in result.output
    
    def test_progress_mixed_checkbox_formats(self, runner, temp_project):
        """Test progress command handles different checkbox formats."""
        ctx = make_context(temp_project)
        
        # Setup
        runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
        runner.invoke(
            cli,
            ["create", "--id", "SPRINT-PROG5", "--title", "Mixed Format", "--author", "test@example.com"],
            obj=ctx
        )
        
        # Add plan.md with mixed formats
        from pathlib import Path
        sprint_path = temp_project / "stride" / "sprints" / "proposed" / "SPRINT-PROG5"
        plan_file = sprint_path / "plan.md"
        plan_file.write_text("""# Tasks

- [x] Lowercase x
- [X] Uppercase X
- [ ] Incomplete
* [x] Asterisk format
  - [x] Indented task
""", encoding="utf-8")
        
        # Act
        result = runner.invoke(cli, ["progress", "SPRINT-PROG5"], obj=ctx)
        
        # Assert
        assert result.exit_code == 0
        # Should parse 5 tasks with 4 completed
        assert "4 / 5" in result.output or "80" in result.output
    
    def test_progress_invalid_sprint(self, runner, temp_project):
        """Test progress command with non-existent sprint."""
        ctx = make_context(temp_project)
        
        # Setup
        runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
        
        # Act
        result = runner.invoke(cli, ["progress", "SPRINT-NONE"], obj=ctx)
        
        # Assert
        assert result.exit_code != 0
        assert "not found" in result.output.lower() or "error" in result.output.lower()
    
    def test_progress_shows_timestamps(self, runner, temp_project):
        """Test progress command displays creation and update timestamps."""
        ctx = make_context(temp_project)
        
        # Setup
        runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
        runner.invoke(
            cli,
            ["create", "--id", "SPRINT-PROG6", "--title", "Timestamps", "--author", "test@example.com"],
            obj=ctx
        )
        
        # Act
        result = runner.invoke(cli, ["progress", "SPRINT-PROG6"], obj=ctx)
        
        # Assert
        assert result.exit_code == 0
        assert "Created:" in result.output or "created" in result.output.lower()
        assert "Updated:" in result.output or "updated" in result.output.lower()


class TestShowCommand:
    """Test stride show command for Sprint 10."""
    
    def test_show_displays_sprint_metadata(self, runner, temp_project):
        """Test show command displays complete sprint metadata."""
        ctx = make_context(temp_project)
        
        # Setup: init and create sprint
        runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
        runner.invoke(
            cli,
            ["create", "--id", "SPRINT-SHOW", "--title", "Show Test Sprint", "--author", "test@example.com"],
            obj=ctx
        )
        
        # Act: show sprint
        result = runner.invoke(cli, ["show", "SPRINT-SHOW"], obj=ctx)
        
        # Assert: metadata displayed
        assert result.exit_code == 0
        assert "SPRINT-SHOW" in result.output
        assert "Show Test Sprint" in result.output
        assert "test@example.com" in result.output
        assert "proposed" in result.output.lower()
    
    def test_show_lists_all_files(self, runner, temp_project):
        """Test show command lists all sprint files with existence status."""
        ctx = make_context(temp_project)
        
        # Setup
        runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
        runner.invoke(
            cli,
            ["create", "--id", "SPRINT-FILE", "--title", "File Test", "--author", "test@example.com"],
            obj=ctx
        )
        
        # Act
        result = runner.invoke(cli, ["show", "SPRINT-FILE"], obj=ctx)
        
        # Assert: all file types mentioned
        assert result.exit_code == 0
        assert "proposal.md" in result.output
        assert "plan.md" in result.output
        assert "design.md" in result.output
        assert "implementation.md" in result.output
        assert "retrospective.md" in result.output
    
    def test_show_with_file_option_displays_content(self, runner, temp_project):
        """Test show --file option displays specific file content."""
        ctx = make_context(temp_project)
        
        # Setup
        runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
        runner.invoke(
            cli,
            ["create", "--id", "SPRINT-VIEW", "--title", "View Test", "--author", "test@example.com"],
            obj=ctx
        )
        
        # Act: show with --file option
        result = runner.invoke(cli, ["show", "SPRINT-VIEW", "--file", "proposal"], obj=ctx)
        
        # Assert: proposal content displayed
        assert result.exit_code == 0
        assert "SPRINT-VIEW" in result.output
        assert "Objectives" in result.output or "objectives" in result.output.lower()
        assert "Success Criteria" in result.output or "success criteria" in result.output.lower()
    
    def test_show_invalid_sprint_id(self, runner, temp_project):
        """Test show command with non-existent sprint ID."""
        ctx = make_context(temp_project)
        
        # Setup: init only, no sprint created
        runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
        
        # Act: show non-existent sprint
        result = runner.invoke(cli, ["show", "SPRINT-NONE"], obj=ctx)
        
        # Assert: error message
        assert result.exit_code != 0
        assert "not found" in result.output.lower() or "error" in result.output.lower()
    
    def test_show_invalid_file_type(self, runner, temp_project):
        """Test show command with invalid file type."""
        ctx = make_context(temp_project)
        
        # Setup
        runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
        runner.invoke(
            cli,
            ["create", "--id", "SPRINT-BADFILE", "--title", "Bad File Test", "--author", "test@example.com"],
            obj=ctx
        )
        
        # Act: show with invalid file type
        result = runner.invoke(cli, ["show", "SPRINT-BADFILE", "--file", "invalid"], obj=ctx)
        
        # Assert: error message about invalid file type
        assert result.exit_code != 0
        assert "invalid" in result.output.lower() or "must be one of" in result.output.lower()
    
    def test_show_displays_file_sizes(self, runner, temp_project):
        """Test show command displays file sizes for existing files."""
        ctx = make_context(temp_project)
        
        # Setup
        runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
        runner.invoke(
            cli,
            ["create", "--id", "SPRINT-SIZE", "--title", "Size Test", "--author", "test@example.com"],
            obj=ctx
        )
        
        # Act
        result = runner.invoke(cli, ["show", "SPRINT-SIZE"], obj=ctx)
        
        # Assert: file size shown (proposal.md is created by default)
        assert result.exit_code == 0
        # Should show bytes for existing files
        assert "bytes" in result.output.lower() or "kb" in result.output.lower() or "✅" in result.output
    
    def test_show_warns_about_missing_files(self, runner, temp_project):
        """Test show command warns about missing files."""
        ctx = make_context(temp_project)
        
        # Setup
        runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
        runner.invoke(
            cli,
            ["create", "--id", "SPRINT-MISS", "--title", "Missing Test", "--author", "test@example.com"],
            obj=ctx
        )
        
        # Act
        result = runner.invoke(cli, ["show", "SPRINT-MISS"], obj=ctx)
        
        # Assert: warnings for missing files
        assert result.exit_code == 0
        # Should have warnings for plan, design, implementation, retrospective
        assert "not found" in result.output.lower() or "⚠" in result.output
    
    def test_show_with_completed_sprint(self, runner, temp_project):
        """Test show command works with completed sprints."""
        ctx = make_context(temp_project)
        
        # Setup: create and complete sprint
        runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
        runner.invoke(
            cli,
            ["create", "--id", "SPRINT-DONE", "--title", "Completed Test", "--author", "test@example.com"],
            obj=ctx
        )
        runner.invoke(cli, ["start", "SPRINT-DONE"], obj=ctx)
        runner.invoke(cli, ["complete", "SPRINT-DONE"], obj=ctx)
        
        # Act: show completed sprint
        result = runner.invoke(cli, ["show", "SPRINT-DONE"], obj=ctx)
        
        # Assert: shows completed status
        assert result.exit_code == 0
        assert "SPRINT-DONE" in result.output
        assert "completed" in result.output.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
