"""
Windsurf Configurator

Configures Stride integration for Windsurf AI editor.

Integration Type: Slash Commands Only (Markdown workflows)
Files Created:
- .windsurf/workflows/stride-*.md (9 workflow files)

Note: Windsurf uses Markdown format with YAML frontmatter, not TOML.
"""

from pathlib import Path
from ..configurator import ToolConfigurator, ConfigResult, ValidationResult
from ..templates import TemplateManager
from ..markers import ManagedMarkerSystem


class WindsurfConfigurator(ToolConfigurator):
    """Configurator for Windsurf."""
    
    @property
    def name(self) -> str:
        return "Windsurf"
    
    @property
    def slug(self) -> str:
        return "windsurf"
    
    @property
    def config_file_name(self) -> None:
        return None  # Windsurf doesn't use root config
    
    @property
    def slash_command_dir(self) -> str:
        return ".windsurf/workflows"
    
    @property
    def command_format(self) -> str:
        return "markdown"
    
    @property
    def priority(self) -> str:
        return "high"
    
    def configure(self, project_path: Path) -> ConfigResult:
        """Create Windsurf workflow files."""
        messages = []
        files_created = []
        
        try:
            # Create workflows directory
            workflows_dir = project_path / self.slash_command_dir
            workflows_dir.mkdir(parents=True, exist_ok=True)
            
            # Create all 9 workflow files (Markdown format)
            workflows = TemplateManager.WORKFLOWS
            for workflow in workflows:
                md_content = TemplateManager.get_slash_command_markdown(workflow)
                md_path = workflows_dir / f"stride-{workflow}.md"
                
                success, message = ManagedMarkerSystem.update_file_with_markers(
                    md_path,
                    md_content,
                    file_type="markdown"
                )
                
                if success:
                    messages.append(f"  ✓ stride-{workflow}.md")
                    files_created.append(md_path)
                else:
                    messages.append(f"  ✗ {message}")
            
            messages.insert(0, f"✓ Created {len(workflows)} workflows in {self.slash_command_dir}/")
            
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
        """Validate Windsurf integration."""
        issues = []
        warnings = []
        
        workflows_dir = project_path / self.slash_command_dir
        if not workflows_dir.exists():
            issues.append(f"Missing directory: {self.slash_command_dir}/")
        else:
            for workflow in TemplateManager.WORKFLOWS:
                md_path = workflows_dir / f"stride-{workflow}.md"
                if not md_path.exists():
                    issues.append(f"Missing stride-{workflow}.md")
                else:
                    valid, message = ManagedMarkerSystem.validate_markers(md_path, "markdown")
                    if not valid:
                        warnings.append(message)
        
        return ValidationResult(
            valid=len(issues) == 0,
            issues=issues,
            warnings=warnings
        )
    
    def update(self, project_path: Path) -> ConfigResult:
        """Update Windsurf workflows."""
        return self.configure(project_path)
