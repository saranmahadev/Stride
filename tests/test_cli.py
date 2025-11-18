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
        
        result = runner.invoke(cli, ["list"], obj=make_context(temp_project))
        
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
                ["list", "--status", "active"],
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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
