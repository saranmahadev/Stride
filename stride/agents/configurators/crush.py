"""
Crush Configurator

Configures Stride integration for Crush.

Integration Type: Root Config Only
Files Created:
- CRUSH.md (root config with managed block)
"""

from pathlib import Path
from ..configurator import ToolConfigurator, ConfigResult, ValidationResult
from ..templates import TemplateManager
from ..markers import ManagedMarkerSystem


class CrushConfigurator(ToolConfigurator):
    """Configurator for Crush."""
    
    @property
    def name(self) -> str:
        return "Crush"
    
    @property
    def slug(self) -> str:
        return "crush"
    
    @property
    def config_file_name(self) -> str:
        return "CRUSH.md"
    
    @property
    def slash_command_dir(self) -> None:
        return None
    
    @property
    def command_format(self) -> None:
        return None
    
    @property
    def priority(self) -> str:
        return "medium"
    
    def configure(self, project_path: Path) -> ConfigResult:
        """Create Crush root config file."""
        messages = []
        files_created = []
        
        try:
            root_config_path = project_path / self.config_file_name
            root_content = TemplateManager.get_root_stub(self.name)
            
            success, message = ManagedMarkerSystem.update_file_with_markers(
                root_config_path, root_content, file_type="markdown"
            )
            
            if success:
                messages.append(f"✓ {message}")
                files_created.append(root_config_path)
                return ConfigResult(success=True, messages=messages, files_created=files_created)
            else:
                return ConfigResult(success=False, messages=[message])
            
        except Exception as e:
            return ConfigResult(success=False, messages=[f"Error configuring {self.name}: {str(e)}"])
    
    def validate(self, project_path: Path) -> ValidationResult:
        """Validate Crush integration."""
        issues = []
        warnings = []
        
        root_path = project_path / self.config_file_name
        if not root_path.exists():
            issues.append(f"Missing {self.config_file_name}")
        else:
            valid, message = ManagedMarkerSystem.validate_markers(root_path, "markdown")
            if not valid:
                issues.append(message)
        
        return ValidationResult(valid=len(issues) == 0, issues=issues, warnings=warnings)
    
    def update(self, project_path: Path) -> ConfigResult:
        """Update Crush integration."""
        return self.configure(project_path)
