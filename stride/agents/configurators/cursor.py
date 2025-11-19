"""
Cursor Configurator

Configures Stride integration for Cursor AI editor.

Integration Type: Hybrid (root config + slash commands)
Files Created:
- CURSOR.md (root config with managed block)
- .cursor/prompts/stride-*.toml (9 workflow commands)
"""

from pathlib import Path
from ..configurator import ToolConfigurator, ConfigResult, ValidationResult
from ..templates import TemplateManager
from ..markers import ManagedMarkerSystem


class CursorConfigurator(ToolConfigurator):
    """Configurator for Cursor AI."""
    
    @property
    def name(self) -> str:
        return "Cursor"
    
    @property
    def slug(self) -> str:
        return "cursor"
    
    @property
    def config_file_name(self) -> str:
        return "CURSOR.md"
    
    @property
    def slash_command_dir(self) -> str:
        return ".cursor/prompts"
    
    @property
    def command_format(self) -> str:
        return "toml"
    
    @property
    def priority(self) -> str:
        return "high"
    
    def configure(self, project_path: Path) -> ConfigResult:
        """Create Cursor integration files."""
        messages = []
        files_created = []
        
        try:
            # 1. Create root config
            root_config_path = project_path / self.config_file_name
            root_content = TemplateManager.get_root_stub(self.name)
            
            success, message = ManagedMarkerSystem.update_file_with_markers(
                root_config_path,
                root_content,
                file_type="markdown"
            )
            
            if success:
                messages.append(f"✓ {message}")
                files_created.append(root_config_path)
            else:
                return ConfigResult(success=False, messages=[message])
            
            # 2. Create slash commands
            slash_dir = project_path / self.slash_command_dir
            slash_dir.mkdir(parents=True, exist_ok=True)
            
            workflows = TemplateManager.WORKFLOWS
            for workflow in workflows:
                toml_content = TemplateManager.get_slash_command_toml(workflow)
                toml_path = slash_dir / f"stride-{workflow}.toml"
                
                success, message = ManagedMarkerSystem.update_file_with_markers(
                    toml_path,
                    toml_content,
                    file_type="toml"
                )
                
                if success:
                    messages.append(f"  ✓ stride-{workflow}.toml")
                    files_created.append(toml_path)
            
            messages.append(f"✓ Created {len(workflows)} slash commands")
            
            return ConfigResult(
                success=True,
                messages=messages,
                files_created=files_created
            )
            
        except Exception as e:
            return ConfigResult(
                success=False,
                messages=[f"Error configuring {self.name}: {str(e)}"]
            )
    
    def validate(self, project_path: Path) -> ValidationResult:
        """Validate Cursor integration."""
        issues = []
        warnings = []
        
        root_path = project_path / self.config_file_name
        if not root_path.exists():
            issues.append(f"Missing {self.config_file_name}")
        else:
            valid, message = ManagedMarkerSystem.validate_markers(root_path, "markdown")
            if not valid:
                issues.append(message)
        
        slash_dir = project_path / self.slash_command_dir
        if not slash_dir.exists():
            issues.append(f"Missing directory: {self.slash_command_dir}/")
        else:
            for workflow in TemplateManager.WORKFLOWS:
                toml_path = slash_dir / f"stride-{workflow}.toml"
                if not toml_path.exists():
                    issues.append(f"Missing stride-{workflow}.toml")
                else:
                    valid, message = ManagedMarkerSystem.validate_markers(toml_path, "toml")
                    if not valid:
                        warnings.append(message)
        
        return ValidationResult(
            valid=len(issues) == 0,
            issues=issues,
            warnings=warnings
        )
    
    def update(self, project_path: Path) -> ConfigResult:
        """Update Cursor integration."""
        return self.configure(project_path)
