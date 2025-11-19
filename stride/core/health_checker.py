"""
Health checker for Stride projects.

Performs comprehensive diagnostics on Stride installation, project structure,
sprint integrity, and configuration to identify issues and suggest fixes.
"""

import sys
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import importlib.metadata

from .folder_manager import FolderManager, SprintStatus
from .config_manager import ConfigManager
from .metadata_manager import MetadataManager
from .config_schemas import USER_CONFIG_SCHEMA, PROJECT_CONFIG_SCHEMA


class CheckStatus(Enum):
    """Status of a health check."""
    PASS = "pass"
    WARNING = "warning"
    ERROR = "error"
    INFO = "info"


@dataclass
class HealthCheckResult:
    """Result of a single health check."""
    category: str
    check_name: str
    status: CheckStatus
    message: str
    details: Optional[str] = None
    fix_suggestion: Optional[str] = None
    auto_fixable: bool = False
    
    @property
    def icon(self) -> str:
        """Get icon for check status."""
        if self.status == CheckStatus.PASS:
            return "✓"
        elif self.status == CheckStatus.WARNING:
            return "⚠"
        elif self.status == CheckStatus.ERROR:
            return "✗"
        else:
            return "ℹ"


@dataclass
class HealthReport:
    """Complete health check report."""
    results: List[HealthCheckResult] = field(default_factory=list)
    
    def add_result(self, result: HealthCheckResult) -> None:
        """Add a check result to the report."""
        self.results.append(result)
    
    def add_check(
        self,
        category: str,
        check_name: str,
        status: CheckStatus,
        message: str,
        details: Optional[str] = None,
        fix_suggestion: Optional[str] = None,
        auto_fixable: bool = False,
    ) -> None:
        """Add a check result using individual parameters."""
        result = HealthCheckResult(
            category=category,
            check_name=check_name,
            status=status,
            message=message,
            details=details,
            fix_suggestion=fix_suggestion,
            auto_fixable=auto_fixable,
        )
        self.add_result(result)
    
    @property
    def passed_count(self) -> int:
        """Count of passed checks."""
        return sum(1 for r in self.results if r.status == CheckStatus.PASS)
    
    @property
    def warning_count(self) -> int:
        """Count of warning checks."""
        return sum(1 for r in self.results if r.status == CheckStatus.WARNING)
    
    @property
    def error_count(self) -> int:
        """Count of error checks."""
        return sum(1 for r in self.results if r.status == CheckStatus.ERROR)
    
    @property
    def total_checks(self) -> int:
        """Total number of checks performed."""
        return len([r for r in self.results if r.status != CheckStatus.INFO])
    
    @property
    def health_score(self) -> int:
        """Calculate overall health score (0-100)."""
        if self.total_checks == 0:
            return 100
        
        # Weight: pass=1, warning=0.5, error=0
        score = (self.passed_count + (self.warning_count * 0.5)) / self.total_checks
        return int(score * 100)
    
    @property
    def health_grade(self) -> str:
        """Get health grade based on score."""
        score = self.health_score
        if score >= 90:
            return "Excellent"
        elif score >= 75:
            return "Good"
        elif score >= 60:
            return "Fair"
        elif score >= 40:
            return "Poor"
        else:
            return "Critical"
    
    def get_by_category(self, category: str) -> List[HealthCheckResult]:
        """Get all results for a specific category."""
        return [r for r in self.results if r.category == category]
    
    def get_fixable_issues(self) -> List[HealthCheckResult]:
        """Get all issues that can be auto-fixed."""
        return [r for r in self.results if r.auto_fixable and r.status != CheckStatus.PASS]


class HealthChecker:
    """
    Performs comprehensive health checks on Stride projects.
    
    Checks installation, project structure, sprint integrity,
    configuration, and dependencies.
    """
    
    REQUIRED_PACKAGES = [
        'click',
        'PyYAML',
        'Jinja2',
        'python-dateutil',
        'colorama',
        'rich',
        'watchdog',
    ]
    
    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize health checker.
        
        Args:
            project_root: Project root directory (defaults to current directory)
        """
        self.project_root = project_root or Path.cwd()
        self.report = HealthReport()
    
    def check_all(self) -> HealthReport:
        """
        Run all health checks.
        
        Returns:
            Complete health report
        """
        self.report = HealthReport()
        
        self.check_installation()
        self.check_project_structure()
        self.check_sprints()
        self.check_configuration()
        
        return self.report
    
    def check_installation(self) -> None:
        """Check Python version and installed dependencies."""
        category = "Installation"
        
        # Python version
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        if sys.version_info >= (3, 8):
            self.report.add_check(
                category,
                "python_version",
                CheckStatus.PASS,
                f"Python {python_version}",
            )
        else:
            self.report.add_check(
                category,
                "python_version",
                CheckStatus.ERROR,
                f"Python {python_version} (requires 3.8+)",
                fix_suggestion="Upgrade to Python 3.8 or higher",
            )
        
        # Stride version
        try:
            stride_version = importlib.metadata.version('stride-cli')
            self.report.add_check(
                category,
                "stride_version",
                CheckStatus.PASS,
                f"Stride version {stride_version}",
            )
        except importlib.metadata.PackageNotFoundError:
            # Running from source
            self.report.add_check(
                category,
                "stride_version",
                CheckStatus.INFO,
                "Running from source (not installed)",
            )
        
        # Check dependencies
        missing_packages = []
        for package in self.REQUIRED_PACKAGES:
            try:
                importlib.metadata.version(package)
            except importlib.metadata.PackageNotFoundError:
                missing_packages.append(package)
        
        if not missing_packages:
            self.report.add_check(
                category,
                "dependencies",
                CheckStatus.PASS,
                f"All {len(self.REQUIRED_PACKAGES)} dependencies installed",
            )
        else:
            self.report.add_check(
                category,
                "dependencies",
                CheckStatus.ERROR,
                f"Missing {len(missing_packages)} package(s): {', '.join(missing_packages)}",
                fix_suggestion=f"pip install {' '.join(missing_packages)}",
                auto_fixable=True,
            )
    
    def check_project_structure(self) -> None:
        """Check project folder structure and required files."""
        category = "Project Structure"
        
        stride_root = self.project_root / "stride"
        
        # Check if Stride is initialized
        if not stride_root.exists():
            self.report.add_check(
                category,
                "stride_initialized",
                CheckStatus.ERROR,
                "Stride not initialized",
                fix_suggestion="Run: stride init",
                auto_fixable=True,
            )
            return
        
        self.report.add_check(
            category,
            "stride_initialized",
            CheckStatus.PASS,
            "Stride initialized",
        )
        
        # Check required directories
        required_dirs = [
            ("sprints", "Sprint folders"),
            ("specs", "Specifications"),
            ("introspection", "Introspection data"),
        ]
        
        for dir_name, description in required_dirs:
            dir_path = stride_root / dir_name
            if dir_path.exists() and dir_path.is_dir():
                self.report.add_check(
                    category,
                    f"dir_{dir_name}",
                    CheckStatus.PASS,
                    f"{description} folder exists",
                )
            else:
                self.report.add_check(
                    category,
                    f"dir_{dir_name}",
                    CheckStatus.ERROR,
                    f"{description} folder missing",
                    fix_suggestion=f"Create directory: {dir_path}",
                    auto_fixable=True,
                )
        
        # Check status folders
        sprints_root = stride_root / "sprints"
        if sprints_root.exists():
            for status in SprintStatus:
                status_path = sprints_root / status.value
                if status_path.exists() and status_path.is_dir():
                    self.report.add_check(
                        category,
                        f"status_{status.value}",
                        CheckStatus.PASS,
                        f"{status.value}/ folder exists",
                    )
                else:
                    self.report.add_check(
                        category,
                        f"status_{status.value}",
                        CheckStatus.ERROR,
                        f"{status.value}/ folder missing",
                        fix_suggestion=f"Create directory: {status_path}",
                        auto_fixable=True,
                    )
        
        # Check for project.md
        project_md = stride_root / "project.md"
        if project_md.exists():
            self.report.add_check(
                category,
                "project_md",
                CheckStatus.PASS,
                "project.md exists",
            )
        else:
            self.report.add_check(
                category,
                "project_md",
                CheckStatus.WARNING,
                "project.md not found",
                fix_suggestion="Create project.md to document project overview",
                auto_fixable=True,
            )
    
    def check_sprints(self) -> None:
        """Check sprint integrity and consistency."""
        category = "Sprints"
        
        stride_root = self.project_root / "stride"
        if not stride_root.exists():
            return
        
        fm = FolderManager(self.project_root)
        
        # Count sprints
        total_sprints = 0
        sprint_issues = []
        
        for status in SprintStatus:
            status_path = fm.sprints_root / status.value
            if not status_path.exists():
                continue
            
            for sprint_dir in status_path.iterdir():
                if not sprint_dir.is_dir():
                    continue
                
                total_sprints += 1
                sprint_id = sprint_dir.name
                
                # Check proposal.md exists
                proposal_file = sprint_dir / "proposal.md"
                if not proposal_file.exists():
                    sprint_issues.append(f"{sprint_id}: Missing proposal.md")
                    continue
                
                # Check metadata
                try:
                    metadata, _ = MetadataManager.parse_file(proposal_file)
                    
                    # Check required fields
                    if 'id' not in metadata:
                        sprint_issues.append(f"{sprint_id}: Missing 'id' in metadata")
                    elif metadata['id'] != sprint_id:
                        sprint_issues.append(f"{sprint_id}: ID mismatch (metadata says {metadata['id']})")
                    
                    if 'status' not in metadata:
                        sprint_issues.append(f"{sprint_id}: Missing 'status' in metadata")
                    elif metadata['status'] != status.value:
                        sprint_issues.append(f"{sprint_id}: Status mismatch (folder={status.value}, metadata={metadata['status']})")
                    
                    # Check recommended fields
                    if 'priority' not in metadata:
                        sprint_issues.append(f"{sprint_id}: Missing 'priority' field")
                    
                except Exception as e:
                    sprint_issues.append(f"{sprint_id}: Invalid metadata ({str(e)})")
        
        # Report sprint count
        if total_sprints > 0:
            self.report.add_check(
                category,
                "sprint_count",
                CheckStatus.INFO,
                f"Found {total_sprints} sprint(s)",
            )
        else:
            self.report.add_check(
                category,
                "sprint_count",
                CheckStatus.WARNING,
                "No sprints found",
                details="Project has no sprints yet",
            )
        
        # Report issues
        if sprint_issues:
            status = CheckStatus.WARNING if len(sprint_issues) < 5 else CheckStatus.ERROR
            self.report.add_check(
                category,
                "sprint_integrity",
                status,
                f"Found {len(sprint_issues)} sprint issue(s)",
                details="\n".join(f"  • {issue}" for issue in sprint_issues[:10]),
                fix_suggestion="Fix sprint metadata and file issues",
            )
        elif total_sprints > 0:
            self.report.add_check(
                category,
                "sprint_integrity",
                CheckStatus.PASS,
                "All sprints have valid structure",
            )
    
    def check_configuration(self) -> None:
        """Check configuration files and settings."""
        category = "Configuration"
        
        cm = ConfigManager(self.project_root)
        
        # Check user config
        user_config_path = Path.home() / ".stride" / "config.yaml"
        if user_config_path.exists():
            try:
                user_config = cm.load_config(user_config_path)
                is_valid, errors = cm.validate_config(user_config, USER_CONFIG_SCHEMA)
                
                if is_valid:
                    self.report.add_check(
                        category,
                        "user_config",
                        CheckStatus.PASS,
                        "User config valid",
                    )
                else:
                    self.report.add_check(
                        category,
                        "user_config",
                        CheckStatus.ERROR,
                        "User config has errors",
                        details="\n".join(f"  • {err}" for err in errors[:5]),
                        fix_suggestion="Fix validation errors in ~/.stride/config.yaml",
                    )
            except Exception as e:
                self.report.add_check(
                    category,
                    "user_config",
                    CheckStatus.ERROR,
                    f"User config invalid: {str(e)}",
                    fix_suggestion="Fix or recreate ~/.stride/config.yaml",
                )
        else:
            self.report.add_check(
                category,
                "user_config",
                CheckStatus.WARNING,
                "User config not found",
                fix_suggestion="Run: stride login",
                auto_fixable=True,
            )
        
        # Check project config
        project_config_path = self.project_root / "stride.config.yaml"
        if project_config_path.exists():
            try:
                project_config = cm.load_config(project_config_path)
                is_valid, errors = cm.validate_config(project_config, PROJECT_CONFIG_SCHEMA)
                
                if is_valid:
                    self.report.add_check(
                        category,
                        "project_config",
                        CheckStatus.PASS,
                        "Project config valid",
                    )
                    
                    # Check agents
                    agents = project_config.get("project", {}).get("agents", [])
                    if agents:
                        self.report.add_check(
                            category,
                            "agents",
                            CheckStatus.INFO,
                            f"{len(agents)} agent(s) configured",
                        )
                    else:
                        self.report.add_check(
                            category,
                            "agents",
                            CheckStatus.WARNING,
                            "No agents configured",
                            fix_suggestion="Add agents with: stride config set project.agents",
                        )
                else:
                    self.report.add_check(
                        category,
                        "project_config",
                        CheckStatus.ERROR,
                        "Project config has errors",
                        details="\n".join(f"  • {err}" for err in errors[:5]),
                        fix_suggestion="Fix validation errors in stride.config.yaml",
                    )
            except Exception as e:
                self.report.add_check(
                    category,
                    "project_config",
                    CheckStatus.ERROR,
                    f"Project config invalid: {str(e)}",
                    fix_suggestion="Fix or recreate stride.config.yaml",
                )
        else:
            self.report.add_check(
                category,
                "project_config",
                CheckStatus.INFO,
                "Project config not found (optional)",
            )
