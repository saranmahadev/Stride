"""
Universal AGENTS.md Configurator

Creates the universal fallback AGENTS.md file in stride/ directory.
This file contains complete workflow documentation for all 9 Stride commands.

Integration Type: Universal fallback
Files Created:
- stride/AGENTS.md (complete workflow documentation)
"""

from pathlib import Path
from ..configurator import ToolConfigurator, ConfigResult, ValidationResult
from ..templates import TemplateManager
from ..markers import ManagedMarkerSystem


class UniversalConfigurator(ToolConfigurator):
    """Configurator for Universal AGENTS.md fallback."""
    
    @property
    def name(self) -> str:
        return "Universal AGENTS.md"
    
    @property
    def slug(self) -> str:
        return "universal"
    
    @property
    def config_file_name(self) -> str:
        return "stride/AGENTS.md"
    
    @property
    def slash_command_dir(self) -> None:
        return None
    
    @property
    def command_format(self) -> None:
        return None
    
    @property
    def priority(self) -> str:
        return "high"  # Critical fallback file
    
    def configure(self, project_path: Path) -> ConfigResult:
        """Create universal AGENTS.md file."""
        messages = []
        files_created = []
        
        try:
            # Ensure stride directory exists
            stride_dir = project_path / "stride"
            stride_dir.mkdir(parents=True, exist_ok=True)
            
            agents_md_path = project_path / self.config_file_name
            full_content = TemplateManager.get_full_agents_md()
            
            success, message = ManagedMarkerSystem.update_file_with_markers(
                agents_md_path, full_content, file_type="markdown"
            )
            
            if success:
                messages.append(f"✓ {message}")
                files_created.append(agents_md_path)
                return ConfigResult(success=True, messages=messages, files_created=files_created)
            else:
                return ConfigResult(success=False, messages=[message])
            
        except Exception as e:
            return ConfigResult(success=False, messages=[f"Error configuring {self.name}: {str(e)}"])
    
    def validate(self, project_path: Path) -> ValidationResult:
        """Validate universal AGENTS.md file."""
        issues = []
        warnings = []
        
        agents_md_path = project_path / self.config_file_name
        if not agents_md_path.exists():
            issues.append(f"Missing {self.config_file_name}")
        else:
            valid, message = ManagedMarkerSystem.validate_markers(agents_md_path, "markdown")
            if not valid:
                issues.append(message)
        
        return ValidationResult(valid=len(issues) == 0, issues=issues, warnings=warnings)
    
    def update(self, project_path: Path) -> ConfigResult:
        """Update universal AGENTS.md file."""
        return self.configure(project_path)
