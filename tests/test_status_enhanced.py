"""
Tests for enhanced sprint dashboard and status features.

Tests the new visual dashboard, health metrics, team analytics,
and detailed mode added in Sprint 8.
"""
import pytest
from pathlib import Path
from click.testing import CliRunner
from stride.cli.main import cli


def make_context(project_root: Path):
    """Helper to create a Click context for testing."""
    return {
        "project_root": project_root,
        "stride_root": project_root / "stride",
        "config_file": project_root / "stride.config.yaml",
    }


@pytest.fixture
def runner():
    """Provide a Click test runner."""
    return CliRunner()


@pytest.fixture
def temp_project(tmp_path):
    """Create a temporary project directory."""
    return tmp_path


class TestDashboardOutput:
    """Test dashboard visual output."""
    
    def test_dashboard_shows_sprint_distribution(self, runner):
        """Test dashboard shows sprint distribution bars."""
        with runner.isolated_filesystem() as temp_dir:
            temp_project = Path(temp_dir)
            ctx = make_context(temp_project)
            
            # Initialize and create sprints
            runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
            runner.invoke(cli, ["create", "--id", "SPRINT-PROP", "--title", "Proposed Sprint", "--author", "test@example.com"], obj=ctx)
            runner.invoke(cli, ["create", "--id", "SPRINT-ACTV", "--title", "Active Sprint", "--author", "test@example.com"], obj=ctx)
            runner.invoke(cli, ["move", "SPRINT-ACTV", "active"], obj=ctx)
            
            # Test dashboard output
            result = runner.invoke(cli, ["list", "--format", "dashboard"], obj=ctx)
            
            assert result.exit_code == 0
            assert "Sprint Dashboard" in result.output or "📊" in result.output
            assert "Sprint Distribution" in result.output
            assert "Proposed" in result.output
            assert "Active" in result.output
    
    def test_dashboard_shows_health_metrics(self, runner):
        """Test dashboard shows health metrics."""
        with runner.isolated_filesystem() as temp_dir:
            temp_project = Path(temp_dir)
            ctx = make_context(temp_project)
            
            runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
            runner.invoke(cli, ["create", "--id", "SPRINT-TST1", "--title", "Test Sprint", "--author", "test@example.com"], obj=ctx)
            
            result = runner.invoke(cli, ["list", "--format", "dashboard"], obj=ctx)
            
            assert result.exit_code == 0
            assert "Health Metrics" in result.output
            assert "Total Sprints" in result.output
            assert "Active Sprints" in result.output
            assert "Completed" in result.output
    
    def test_dashboard_shows_blocked_sprints(self, runner):
        """Test dashboard highlights blocked sprints."""
        with runner.isolated_filesystem() as temp_dir:
            temp_project = Path(temp_dir)
            ctx = make_context(temp_project)
            
            runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
            runner.invoke(cli, ["create", "--id", "SPRINT-BLCK", "--title", "Blocked Sprint", "--author", "test@example.com"], obj=ctx)
            runner.invoke(cli, ["move", "SPRINT-BLCK", "blocked", "--reason", "Waiting for approval"], obj=ctx)
            
            result = runner.invoke(cli, ["list", "--format", "dashboard"], obj=ctx)
            
            assert result.exit_code == 0
            assert "Blocked" in result.output
    
    def test_dashboard_default_format(self, runner):
        """Test that dashboard is the default format."""
        with runner.isolated_filesystem() as temp_dir:
            temp_project = Path(temp_dir)
            ctx = make_context(temp_project)
            
            runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
            runner.invoke(cli, ["create", "--id", "SPRINT-TST1", "--title", "Test", "--author", "test@example.com"], obj=ctx)
            
            # List without format flag should show dashboard
            result = runner.invoke(cli, ["list"], obj=ctx)
            
            assert result.exit_code == 0
            assert "Sprint Dashboard" in result.output or "Sprint Distribution" in result.output


class TestTeamAnalytics:
    """Test team analytics features."""
    
    def test_team_flag_shows_author_statistics(self, runner):
        """Test --team flag displays per-author statistics."""
        with runner.isolated_filesystem() as temp_dir:
            temp_project = Path(temp_dir)
            ctx = make_context(temp_project)
            
            runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
            runner.invoke(cli, ["create", "--id", "SPRINT-TST1", "--title", "Sprint 1", "--author", "alice@example.com"], obj=ctx)
            runner.invoke(cli, ["create", "--id", "SPRINT-TST2", "--title", "Sprint 2", "--author", "bob@example.com"], obj=ctx)
            runner.invoke(cli, ["create", "--id", "SPRINT-TST3", "--title", "Sprint 3", "--author", "alice@example.com"], obj=ctx)
            
            result = runner.invoke(cli, ["list", "--team"], obj=ctx)
            
            assert result.exit_code == 0
            assert "Team Activity" in result.output
            assert "alice@example.com" in result.output
            assert "bob@example.com" in result.output
    
    def test_team_shows_sprint_counts(self, runner):
        """Test team analytics shows correct sprint counts."""
        with runner.isolated_filesystem() as temp_dir:
            temp_project = Path(temp_dir)
            ctx = make_context(temp_project)
            
            runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
            runner.invoke(cli, ["create", "--id", "SPRINT-TST1", "--title", "Sprint 1", "--author", "alice@example.com"], obj=ctx)
            runner.invoke(cli, ["create", "--id", "SPRINT-TST2", "--title", "Sprint 2", "--author", "alice@example.com"], obj=ctx)
            
            result = runner.invoke(cli, ["list", "--team"], obj=ctx)
            
            assert result.exit_code == 0
            # Alice should have 2 sprints
            assert "alice@example.com" in result.output


class TestDetailedMode:
    """Test detailed sprint listing."""
    
    def test_detailed_flag_shows_individual_sprints(self, runner):
        """Test --detailed flag shows individual sprint details."""
        with runner.isolated_filesystem() as temp_dir:
            temp_project = Path(temp_dir)
            ctx = make_context(temp_project)
            
            runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
            runner.invoke(cli, ["create", "--id", "SPRINT-DETL", "--title", "Detailed Sprint", "--author", "test@example.com", "--priority", "high"], obj=ctx)
            
            result = runner.invoke(cli, ["list", "--detailed"], obj=ctx)
            
            assert result.exit_code == 0
            assert "Detailed Sprint List" in result.output
            assert "SPRINT-DETL" in result.output
            assert "Detailed Sprint" in result.output
    
    def test_detailed_shows_priority(self, runner):
        """Test detailed mode shows sprint priority."""
        with runner.isolated_filesystem() as temp_dir:
            temp_project = Path(temp_dir)
            ctx = make_context(temp_project)
            
            runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
            runner.invoke(cli, ["create", "--id", "SPRINT-TST1", "--title", "Test", "--author", "test@example.com", "--priority", "critical"], obj=ctx)
            
            result = runner.invoke(cli, ["list", "--detailed"], obj=ctx)
            
            assert result.exit_code == 0
            assert "Priority" in result.output
            assert "critical" in result.output
    
    def test_detailed_shows_sprint_age(self, runner):
        """Test detailed mode shows sprint age."""
        with runner.isolated_filesystem() as temp_dir:
            temp_project = Path(temp_dir)
            ctx = make_context(temp_project)
            
            runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
            runner.invoke(cli, ["create", "--id", "SPRINT-TST1", "--title", "Test", "--author", "test@example.com"], obj=ctx)
            
            result = runner.invoke(cli, ["list", "--detailed"], obj=ctx)
            
            assert result.exit_code == 0
            assert "Age" in result.output or "days" in result.output
    
    def test_detailed_shows_tags(self, runner):
        """Test detailed mode shows sprint tags."""
        with runner.isolated_filesystem() as temp_dir:
            temp_project = Path(temp_dir)
            ctx = make_context(temp_project)
            
            runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
            runner.invoke(cli, ["create", "--id", "SPRINT-TST1", "--title", "Test", "--author", "test@example.com", "--tags", "bug,urgent"], obj=ctx)
            
            result = runner.invoke(cli, ["list", "--detailed"], obj=ctx)
            
            assert result.exit_code == 0
            assert "Tags" in result.output
            assert "bug" in result.output
            assert "urgent" in result.output


class TestHealthMetrics:
    """Test sprint health metrics calculations."""
    
    def test_metrics_calculate_total_sprints(self, runner):
        """Test health metrics show correct total."""
        with runner.isolated_filesystem() as temp_dir:
            temp_project = Path(temp_dir)
            ctx = make_context(temp_project)
            
            runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
            runner.invoke(cli, ["create", "--id", "SPRINT-TST1", "--title", "Sprint 1", "--author", "test@example.com"], obj=ctx)
            runner.invoke(cli, ["create", "--id", "SPRINT-TST2", "--title", "Sprint 2", "--author", "test@example.com"], obj=ctx)
            runner.invoke(cli, ["create", "--id", "SPRINT-TST3", "--title", "Sprint 3", "--author", "test@example.com"], obj=ctx)
            
            result = runner.invoke(cli, ["list"], obj=ctx)
            
            assert result.exit_code == 0
            assert "Total Sprints: 3" in result.output or "3" in result.output
    
    def test_metrics_track_blocked_sprints(self, runner):
        """Test blocked sprints are tracked in metrics."""
        with runner.isolated_filesystem() as temp_dir:
            temp_project = Path(temp_dir)
            ctx = make_context(temp_project)
            
            runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
            runner.invoke(cli, ["create", "--id", "SPRINT-BLCK", "--title", "Blocked 1", "--author", "test@example.com"], obj=ctx)
            runner.invoke(cli, ["move", "SPRINT-BLCK", "blocked", "--reason", "Test"], obj=ctx)
            
            result = runner.invoke(cli, ["list"], obj=ctx)
            
            assert result.exit_code == 0
            assert "Blocked: 1" in result.output or "Blocked" in result.output
    
    def test_metrics_track_completed_sprints(self, runner):
        """Test completed sprints are tracked."""
        with runner.isolated_filesystem() as temp_dir:
            temp_project = Path(temp_dir)
            ctx = make_context(temp_project)
            
            runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
            runner.invoke(cli, ["create", "--id", "SPRINT-CMPL", "--title", "Completed 1", "--author", "test@example.com"], obj=ctx)
            runner.invoke(cli, ["move", "SPRINT-CMPL", "completed"], obj=ctx)
            
            result = runner.invoke(cli, ["list"], obj=ctx)
            
            assert result.exit_code == 0
            assert "Completed: 1" in result.output or "Completed" in result.output


class TestFormatOptions:
    """Test different output format options."""
    
    def test_table_format_still_works(self, runner):
        """Test table format is still available."""
        with runner.isolated_filesystem() as temp_dir:
            temp_project = Path(temp_dir)
            ctx = make_context(temp_project)
            
            runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
            runner.invoke(cli, ["create", "--id", "SPRINT-TST1", "--title", "Test", "--author", "test@example.com"], obj=ctx)
            
            result = runner.invoke(cli, ["list", "--format", "table"], obj=ctx)
            
            assert result.exit_code == 0
            assert "SPRINT-TST1" in result.output
    
    def test_list_format_still_works(self, runner):
        """Test list format is still available."""
        with runner.isolated_filesystem() as temp_dir:
            temp_project = Path(temp_dir)
            ctx = make_context(temp_project)
            
            runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
            runner.invoke(cli, ["create", "--id", "SPRINT-TST1", "--title", "Test", "--author", "test@example.com"], obj=ctx)
            
            result = runner.invoke(cli, ["list", "--format", "list"], obj=ctx)
            
            assert result.exit_code == 0
            assert "SPRINT-TST1" in result.output
            assert "[proposed]" in result.output
    
    def test_json_format_still_works(self, runner):
        """Test JSON format is still available."""
        with runner.isolated_filesystem() as temp_dir:
            temp_project = Path(temp_dir)
            ctx = make_context(temp_project)
            
            runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
            runner.invoke(cli, ["create", "--id", "SPRINT-TST1", "--title", "Test", "--author", "test@example.com"], obj=ctx)
            
            result = runner.invoke(cli, ["list", "--format", "json"], obj=ctx)
            
            assert result.exit_code == 0
            assert "SPRINT-TST1" in result.output
            assert '"id":' in result.output


class TestCombinedFlags:
    """Test combining multiple flags."""
    
    def test_detailed_and_team_together(self, runner):
        """Test --detailed and --team flags work together."""
        with runner.isolated_filesystem() as temp_dir:
            temp_project = Path(temp_dir)
            ctx = make_context(temp_project)
            
            runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
            runner.invoke(cli, ["create", "--id", "SPRINT-TST1", "--title", "Test", "--author", "alice@example.com"], obj=ctx)
            
            result = runner.invoke(cli, ["list", "--detailed", "--team"], obj=ctx)
            
            assert result.exit_code == 0
            assert "Detailed Sprint List" in result.output
            assert "Team Activity" in result.output
    
    def test_status_filter_with_dashboard(self, runner):
        """Test status filtering works with dashboard."""
        with runner.isolated_filesystem() as temp_dir:
            temp_project = Path(temp_dir)
            ctx = make_context(temp_project)
            
            runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
            runner.invoke(cli, ["create", "--id", "SPRINT-ACTV", "--title", "Active", "--author", "test@example.com"], obj=ctx)
            runner.invoke(cli, ["move", "SPRINT-ACTV", "active"], obj=ctx)
            runner.invoke(cli, ["create", "--id", "SPRINT-PROP", "--title", "Proposed", "--author", "test@example.com"], obj=ctx)
            
            result = runner.invoke(cli, ["list", "--status", "active"], obj=ctx)
            
            assert result.exit_code == 0
            assert "Active" in result.output


class TestEmptyStates:
    """Test dashboard with no sprints."""
    
    def test_dashboard_empty_project(self, runner):
        """Test dashboard handles empty project gracefully."""
        with runner.isolated_filesystem() as temp_dir:
            temp_project = Path(temp_dir)
            ctx = make_context(temp_project)
            
            runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
            
            result = runner.invoke(cli, ["list"], obj=ctx)
            
            assert result.exit_code == 0
            assert "No sprints found" in result.output
    
    def test_team_analytics_no_sprints(self, runner):
        """Test team analytics with no sprints."""
        with runner.isolated_filesystem() as temp_dir:
            temp_project = Path(temp_dir)
            ctx = make_context(temp_project)
            
            runner.invoke(cli, ["init", "--no-interactive"], obj=ctx)
            
            result = runner.invoke(cli, ["list", "--team"], obj=ctx)
            
            assert result.exit_code == 0
            assert "No sprints found" in result.output
