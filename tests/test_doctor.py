"""
Tests for doctor command and health checker.
"""
import pytest
from pathlib import Path
from click.testing import CliRunner

from stride.cli.main import cli
from stride.core.health_checker import (
    HealthChecker,
    HealthReport,
    HealthCheckResult,
    CheckStatus,
)


class TestHealthCheckResult:
    """Tests for HealthCheckResult class."""
    
    def test_create_result(self):
        """Test creating a health check result."""
        result = HealthCheckResult(
            category="Installation",
            check_name="python_version",
            status=CheckStatus.PASS,
            message="Python 3.12.4",
        )
        
        assert result.category == "Installation"
        assert result.check_name == "python_version"
        assert result.status == CheckStatus.PASS
        assert result.message == "Python 3.12.4"
    
    def test_result_icons(self):
        """Test status icons."""
        pass_result = HealthCheckResult("Test", "test", CheckStatus.PASS, "Pass")
        assert pass_result.icon == "✓"
        
        warning_result = HealthCheckResult("Test", "test", CheckStatus.WARNING, "Warn")
        assert warning_result.icon == "⚠"
        
        error_result = HealthCheckResult("Test", "test", CheckStatus.ERROR, "Error")
        assert error_result.icon == "✗"
        
        info_result = HealthCheckResult("Test", "test", CheckStatus.INFO, "Info")
        assert info_result.icon == "ℹ"
    
    def test_result_with_fix_suggestion(self):
        """Test result with fix suggestion."""
        result = HealthCheckResult(
            category="Test",
            check_name="test",
            status=CheckStatus.ERROR,
            message="Error",
            fix_suggestion="Run: fix command",
            auto_fixable=True,
        )
        
        assert result.fix_suggestion == "Run: fix command"
        assert result.auto_fixable is True


class TestHealthReport:
    """Tests for HealthReport class."""
    
    def test_empty_report(self):
        """Test empty health report."""
        report = HealthReport()
        
        assert report.total_checks == 0
        assert report.passed_count == 0
        assert report.warning_count == 0
        assert report.error_count == 0
        assert report.health_score == 100  # Empty = perfect
        assert report.health_grade == "Excellent"
    
    def test_add_result(self):
        """Test adding results to report."""
        report = HealthReport()
        
        result = HealthCheckResult("Test", "test1", CheckStatus.PASS, "Pass")
        report.add_result(result)
        
        assert len(report.results) == 1
        assert report.passed_count == 1
    
    def test_add_check(self):
        """Test adding check using helper method."""
        report = HealthReport()
        
        report.add_check(
            "Test",
            "test1",
            CheckStatus.PASS,
            "Pass",
        )
        
        assert len(report.results) == 1
        assert report.passed_count == 1
    
    def test_health_score_calculation(self):
        """Test health score calculation."""
        report = HealthReport()
        
        # All pass = 100%
        report.add_check("Test", "test1", CheckStatus.PASS, "Pass")
        report.add_check("Test", "test2", CheckStatus.PASS, "Pass")
        assert report.health_score == 100
        
        # 1 pass, 1 warning = 75% (warning counts as 0.5)
        report.add_check("Test", "test3", CheckStatus.WARNING, "Warn")
        assert report.health_score == 83  # (2 + 0.5) / 3 = 0.833...
        
        # 1 pass, 1 warning, 1 error = 50%
        report.add_check("Test", "test4", CheckStatus.ERROR, "Error")
        assert report.health_score == 62  # (2 + 0.5 + 0) / 4 = 0.625
    
    def test_health_grade(self):
        """Test health grade assignment."""
        report = HealthReport()
        
        # Excellent (90+)
        for i in range(10):
            report.add_check("Test", f"test{i}", CheckStatus.PASS, "Pass")
        assert report.health_grade == "Excellent"
        assert report.health_score >= 90
        
        # Fair (60-74)
        for i in range(10, 16):
            report.add_check("Test", f"test{i}", CheckStatus.ERROR, "Error")
        assert report.health_grade == "Fair"
        assert 60 <= report.health_score < 75
    
    def test_get_by_category(self):
        """Test filtering results by category."""
        report = HealthReport()
        
        report.add_check("Category1", "test1", CheckStatus.PASS, "Pass")
        report.add_check("Category2", "test2", CheckStatus.PASS, "Pass")
        report.add_check("Category1", "test3", CheckStatus.WARNING, "Warn")
        
        cat1_results = report.get_by_category("Category1")
        assert len(cat1_results) == 2
        
        cat2_results = report.get_by_category("Category2")
        assert len(cat2_results) == 1
    
    def test_get_fixable_issues(self):
        """Test getting fixable issues."""
        report = HealthReport()
        
        report.add_check("Test", "test1", CheckStatus.PASS, "Pass")
        report.add_check("Test", "test2", CheckStatus.ERROR, "Error", auto_fixable=True)
        report.add_check("Test", "test3", CheckStatus.WARNING, "Warn", auto_fixable=True)
        report.add_check("Test", "test4", CheckStatus.ERROR, "Error", auto_fixable=False)
        
        fixable = report.get_fixable_issues()
        assert len(fixable) == 2
        assert all(r.auto_fixable for r in fixable)


class TestHealthChecker:
    """Tests for HealthChecker class."""
    
    def test_checker_initialization(self, tmp_path):
        """Test health checker initialization."""
        checker = HealthChecker(tmp_path)
        
        assert checker.project_root == tmp_path
        assert isinstance(checker.report, HealthReport)
    
    def test_check_installation(self, tmp_path):
        """Test installation checks."""
        checker = HealthChecker(tmp_path)
        checker.check_installation()
        
        results = checker.report.get_by_category("Installation")
        assert len(results) >= 2  # At least Python version and dependencies
        
        # Should have Python version check
        python_check = next((r for r in results if r.check_name == "python_version"), None)
        assert python_check is not None
        assert python_check.status == CheckStatus.PASS  # We're running on 3.8+
    
    def test_check_project_structure_uninitialized(self, tmp_path):
        """Test project structure checks on uninitialized project."""
        checker = HealthChecker(tmp_path)
        checker.check_project_structure()
        
        results = checker.report.get_by_category("Project Structure")
        
        # Should detect uninitialized project
        init_check = next((r for r in results if r.check_name == "stride_initialized"), None)
        assert init_check is not None
        assert init_check.status == CheckStatus.ERROR
    
    def test_check_project_structure_initialized(self, tmp_path):
        """Test project structure checks on initialized project."""
        # Create basic structure
        stride_root = tmp_path / "stride"
        stride_root.mkdir()
        (stride_root / "sprints").mkdir()
        (stride_root / "specs").mkdir()
        (stride_root / "introspection").mkdir()
        
        for status in ["proposed", "active", "blocked", "review", "completed"]:
            (stride_root / "sprints" / status).mkdir()
        
        checker = HealthChecker(tmp_path)
        checker.check_project_structure()
        
        results = checker.report.get_by_category("Project Structure")
        
        # Should pass initialization check
        init_check = next((r for r in results if r.check_name == "stride_initialized"), None)
        assert init_check is not None
        assert init_check.status == CheckStatus.PASS
    
    def test_check_sprints_empty(self, tmp_path):
        """Test sprint checks with no sprints."""
        stride_root = tmp_path / "stride"
        stride_root.mkdir()
        (stride_root / "sprints").mkdir()
        
        for status in ["proposed", "active", "blocked", "review", "completed"]:
            (stride_root / "sprints" / status).mkdir()
        
        checker = HealthChecker(tmp_path)
        checker.check_sprints()
        
        results = checker.report.get_by_category("Sprints")
        
        # Should show warning about no sprints
        count_check = next((r for r in results if r.check_name == "sprint_count"), None)
        assert count_check is not None
        assert count_check.status == CheckStatus.WARNING
    
    def test_check_sprints_with_valid_sprint(self, tmp_path):
        """Test sprint checks with valid sprint."""
        stride_root = tmp_path / "stride"
        stride_root.mkdir()
        sprints_root = stride_root / "sprints"
        sprints_root.mkdir()
        
        for status in ["proposed", "active", "blocked", "review", "completed"]:
            (sprints_root / status).mkdir()
        
        # Create valid sprint
        sprint_dir = sprints_root / "proposed" / "SPRINT-TEST"
        sprint_dir.mkdir()
        
        proposal = sprint_dir / "proposal.md"
        proposal.write_text("""---
id: SPRINT-TEST
title: Test Sprint
status: proposed
created: 2025-01-01T00:00:00Z
priority: high
---

# Test Proposal
""")
        
        checker = HealthChecker(tmp_path)
        checker.check_sprints()
        
        results = checker.report.get_by_category("Sprints")
        
        # Should find sprint
        count_check = next((r for r in results if r.check_name == "sprint_count"), None)
        assert count_check is not None
        assert "1 sprint" in count_check.message
        
        # Should pass integrity check
        integrity_check = next((r for r in results if r.check_name == "sprint_integrity"), None)
        assert integrity_check is not None
        assert integrity_check.status == CheckStatus.PASS
    
    def test_check_all(self, tmp_path):
        """Test running all checks."""
        checker = HealthChecker(tmp_path)
        report = checker.check_all()
        
        assert isinstance(report, HealthReport)
        assert len(report.results) > 0
        
        # Should have results from all categories
        categories = set(r.category for r in report.results)
        assert "Installation" in categories
        assert "Project Structure" in categories


class TestDoctorCommand:
    """Tests for doctor CLI command."""
    
    def test_doctor_command_help(self):
        """Test doctor command help text."""
        runner = CliRunner()
        result = runner.invoke(cli, ['doctor', '--help'])
        
        assert result.exit_code == 0
        assert 'Run health checks' in result.output
        assert '--fix' in result.output
        assert '--verbose' in result.output
        assert '--json' in result.output
    
    def test_doctor_uninitialized_project(self, tmp_path):
        """Test doctor on uninitialized project."""
        runner = CliRunner()
        
        with runner.isolated_filesystem(temp_dir=tmp_path):
            result = runner.invoke(cli, ['doctor'])
            
            assert result.exit_code != 0  # Should fail with errors
            assert 'Health Check' in result.output or 'health' in result.output.lower()
    
    def test_doctor_initialized_project(self, tmp_path):
        """Test doctor on initialized project."""
        runner = CliRunner()
        
        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Initialize project
            runner.invoke(cli, ['init', '--name', 'Test', '--force'])
            
            # Run doctor
            result = runner.invoke(cli, ['doctor'])
            
            assert 'Health' in result.output
            assert 'Installation' in result.output
    
    def test_doctor_json_output(self, tmp_path):
        """Test doctor JSON output."""
        runner = CliRunner()
        
        with runner.isolated_filesystem(temp_dir=tmp_path):
            runner.invoke(cli, ['init', '--name', 'Test', '--force'])
            
            result = runner.invoke(cli, ['doctor', '--json'])
            
            assert result.exit_code in [0, 1]  # May have warnings
            
            # Parse JSON
            import json
            data = json.loads(result.output)
            
            assert 'health_score' in data
            assert 'health_grade' in data
            assert 'total_checks' in data
            assert 'passed' in data
            assert 'warnings' in data
            assert 'errors' in data
            assert 'checks' in data
            assert isinstance(data['checks'], list)
    
    def test_doctor_verbose_mode(self, tmp_path):
        """Test doctor verbose mode."""
        runner = CliRunner()
        
        with runner.isolated_filesystem(temp_dir=tmp_path):
            runner.invoke(cli, ['init', '--name', 'Test', '--force'])
            
            result = runner.invoke(cli, ['doctor', '--verbose'])
            
            assert 'Health' in result.output
            # Verbose should show more details
    
    def test_doctor_fix_flag(self, tmp_path):
        """Test doctor --fix flag."""
        runner = CliRunner()
        
        with runner.isolated_filesystem(temp_dir=tmp_path):
            runner.invoke(cli, ['init', '--name', 'Test', '--force'])
            
            result = runner.invoke(cli, ['doctor', '--fix'])
            
            # Should mention fix attempt or no issues
            assert 'fix' in result.output.lower() or 'Fix' in result.output


class TestHealthCheckerEdgeCases:
    """Tests for edge cases in health checker."""
    
    def test_missing_dependencies_detection(self, tmp_path, monkeypatch):
        """Test detection of missing dependencies."""
        # This is hard to test without actually uninstalling packages
        # So we just verify the check exists
        checker = HealthChecker(tmp_path)
        checker.check_installation()
        
        dep_check = next(
            (r for r in checker.report.results if r.check_name == "dependencies"),
            None
        )
        assert dep_check is not None
    
    def test_sprint_metadata_mismatch(self, tmp_path):
        """Test detection of sprint metadata mismatches."""
        stride_root = tmp_path / "stride"
        sprints_root = stride_root / "sprints"
        sprints_root.mkdir(parents=True)
        
        (sprints_root / "proposed").mkdir()
        
        # Create sprint with ID mismatch
        sprint_dir = sprints_root / "proposed" / "SPRINT-A1B2"
        sprint_dir.mkdir()
        
        proposal = sprint_dir / "proposal.md"
        proposal.write_text("""---
id: SPRINT-WRONG
title: Test
status: proposed
created: 2025-01-01T00:00:00Z
---

# Test
""")
        
        checker = HealthChecker(tmp_path)
        checker.check_sprints()
        
        integrity_check = next(
            (r for r in checker.report.results if r.check_name == "sprint_integrity"),
            None
        )
        assert integrity_check is not None
        assert integrity_check.status in [CheckStatus.WARNING, CheckStatus.ERROR]
        assert "mismatch" in integrity_check.details.lower()
