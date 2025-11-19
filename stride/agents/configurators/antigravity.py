"""
Antigravity Configurator

Configures Stride integration for Antigravity.

Integration Type: Slash Commands Only (Markdown workflows)
Files Created:
- .antigravity/workflows/stride-*.md (9 workflow files)

Note: Antigravity uses Markdown format like Windsurf.
"""

from pathlib import Path
from ..configurator import ToolConfigurator, ConfigResult, ValidationResult
from ..templates import TemplateManager
from ..markers import ManagedMarkerSystem


class AntigravityConfigurator(ToolConfigurator):
    """Configurator for Antigravity."""
    
    @property
    def name(self) -> str:
        return "Antigravity"
    
    @property
    def slug(self) -> str:
        return "antigravity"
    
    @property
    def config_file_name(self) -> None:
        return None
    
    @property
    def slash_command_dir(self) -> str:
        return ".antigravity/workflows"
    
    @property
    def command_format(self) -> str:
        return "markdown"
    
    @property
    def priority(self) -> str:
        return "low"
    
    def configure(self, project_path: Path) -> ConfigResult:
        """Create Antigravity workflow files."""
        messages = []
        files_created = []
        
        try:
            workflows_dir = project_path / self.slash_command_dir
            workflows_dir.mkdir(parents=True, exist_ok=True)
            
            for workflow in TemplateManager.WORKFLOWS:
                md_content = TemplateManager.get_slash_command_markdown(workflow)
                md_path = workflows_dir / f"stride-{workflow}.md"
                
                success, message = ManagedMarkerSystem.update_file_with_markers(
                    md_path, md_content, file_type="markdown"
                )
                
                if success:
                    messages.append(f"  ✓ stride-{workflow}.md")
                    files_created.append(md_path)
            
            messages.insert(0, f"✓ Created {len(TemplateManager.WORKFLOWS)} workflows")
            
            return ConfigResult(success=True, messages=messages, files_created=files_created)
            
        except Exception as e:
            return ConfigResult(success=False, messages=[f"Error configuring {self.name}: {str(e)}"])
    
    def validate(self, project_path: Path) -> ValidationResult:
        """Validate Antigravity integration."""
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
        
        return ValidationResult(valid=len(issues) == 0, issues=issues, warnings=warnings)
    
    def update(self, project_path: Path) -> ConfigResult:
        """Update Antigravity workflows."""
        return self.configure(project_path)
