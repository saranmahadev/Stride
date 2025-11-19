"""
Tests for AI Agent Integration Framework

Tests for:
- Managed marker system
- Template manager
- Tool registry
- Tool configurators
- CLI commands
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from stride.agents.markers import ManagedMarkerSystem
from stride.agents.templates import TemplateManager
from stride.agents.registry import ToolRegistry
from stride.agents.configurators.claude import ClaudeConfigurator
from stride.agents.configurators.windsurf import WindsurfConfigurator
from stride.agents.configurators.cline import ClineConfigurator


class TestManagedMarkerSystem:
    """Tests for managed marker block system."""
    
    def test_has_markers_markdown(self):
        """Test detecting markers in markdown content."""
        content_with_markers = """
# My Project

<!-- STRIDE:START -->
Managed content here
<!-- STRIDE:END -->

Custom content here
"""
        content_without_markers = "# My Project\n\nNo markers here"
        
        assert ManagedMarkerSystem.has_markers(content_with_markers, "markdown")
        assert not ManagedMarkerSystem.has_markers(content_without_markers, "markdown")
    
    def test_has_markers_toml(self):
        """Test detecting markers in TOML content."""
        content_with_markers = """
name = "test"

# STRIDE:START
prompt = "test"
# STRIDE:END
"""
        content_without_markers = 'name = "test"'
        
        assert ManagedMarkerSystem.has_markers(content_with_markers, "toml")
        assert not ManagedMarkerSystem.has_markers(content_without_markers, "toml")
    
    def test_extract_managed_content(self):
        """Test extracting content between markers."""
        content = """
Before
<!-- STRIDE:START -->
Managed content
<!-- STRIDE:END -->
After
"""
        extracted = ManagedMarkerSystem.extract_managed_content(content, "markdown")
        assert extracted == "Managed content"
    
    def test_insert_managed_content_new_file(self):
        """Test inserting markers into new file."""
        new_content = "Test content"
        result = ManagedMarkerSystem.insert_managed_content(
            new_content,
            file_type="markdown"
        )
        
        assert "<!-- STRIDE:START -->" in result
        assert "<!-- STRIDE:END -->" in result
        assert "Test content" in result
    
    def test_insert_managed_content_update_existing(self):
        """Test updating existing managed block."""
        existing = """
Custom header
<!-- STRIDE:START -->
Old content
<!-- STRIDE:END -->
Custom footer
"""
        new_content = "New content"
        result = ManagedMarkerSystem.insert_managed_content(
            new_content,
            file_type="markdown",
            existing_content=existing
        )
        
        assert "Custom header" in result
        assert "Custom footer" in result
        assert "New content" in result
        assert "Old content" not in result
    
    def test_update_file_with_markers(self, tmp_path):
        """Test updating a file with managed markers."""
        test_file = tmp_path / "test.md"
        new_content = "Managed content here"
        
        # Create new file
        success, message = ManagedMarkerSystem.update_file_with_markers(
            test_file,
            new_content,
            file_type="markdown"
        )
        
        assert success
        assert "Created" in message
        assert test_file.exists()
        
        # Update existing file
        updated_content = "Updated content"
        success, message = ManagedMarkerSystem.update_file_with_markers(
            test_file,
            updated_content,
            file_type="markdown"
        )
        
        assert success
        assert "Updated" in message
        
        # Verify content
        content = test_file.read_text()
        assert "Updated content" in content
        assert "<!-- STRIDE:START -->" in content
    
    def test_validate_markers(self, tmp_path):
        """Test marker validation."""
        # Valid file
        valid_file = tmp_path / "valid.md"
        valid_file.write_text("""
<!-- STRIDE:START -->
Content
<!-- STRIDE:END -->
""")
        
        valid, message = ManagedMarkerSystem.validate_markers(valid_file, "markdown")
        assert valid
        
        # Invalid file (missing end marker)
        invalid_file = tmp_path / "invalid.md"
        invalid_file.write_text("""
<!-- STRIDE:START -->
Content
""")
        
        valid, message = ManagedMarkerSystem.validate_markers(invalid_file, "markdown")
        assert not valid


class TestTemplateManager:
    """Tests for template manager."""
    
    def test_workflows_list(self):
        """Test that all 9 workflows are defined."""
        assert len(TemplateManager.WORKFLOWS) == 9
        expected = ['init', 'plan', 'present', 'implement', 'feedback', 
                   'block', 'unblock', 'submit', 'complete']
        assert TemplateManager.WORKFLOWS == expected
    
    def test_get_root_stub(self):
        """Test root stub template generation."""
        stub = TemplateManager.get_root_stub("Claude Code")
        
        assert "# Stride Sprint Management" in stub
        assert "/stride:init" in stub
        assert "/stride:plan" in stub
        assert "/stride:complete" in stub
        assert "stride/AGENTS.md" in stub
    
    def test_get_full_agents_md(self):
        """Test full AGENTS.md template."""
        full_md = TemplateManager.get_full_agents_md()
        
        assert "# Stride AI Agent Integration Guide" in full_md
        assert len(full_md) > 500  # Should be substantial
        
        # Check all 9 workflows are documented
        for workflow in TemplateManager.WORKFLOWS:
            assert f"/stride:{workflow}" in full_md
    
    def test_get_slash_command_toml(self):
        """Test TOML slash command template generation."""
        for workflow in TemplateManager.WORKFLOWS:
            toml = TemplateManager.get_slash_command_toml(workflow)
            
            assert f'name = "stride-{workflow}"' in toml
            assert "# STRIDE:START" in toml
            assert "# STRIDE:END" in toml
            assert "prompt = " in toml
    
    def test_get_slash_command_markdown(self):
        """Test Markdown slash command template generation."""
        for workflow in TemplateManager.WORKFLOWS:
            md = TemplateManager.get_slash_command_markdown(workflow)
            
            assert "---" in md  # YAML frontmatter
            assert "description:" in md
            assert "auto_execution_mode:" in md
            assert "<!-- STRIDE:START -->" in md
            assert "<!-- STRIDE:END -->" in md
    
    def test_get_all_slash_commands_toml(self):
        """Test getting all TOML commands."""
        all_toml = TemplateManager.get_all_slash_commands_toml()
        
        assert len(all_toml) == 9
        for workflow in TemplateManager.WORKFLOWS:
            assert workflow in all_toml
    
    def test_get_all_slash_commands_markdown(self):
        """Test getting all Markdown commands."""
        all_md = TemplateManager.get_all_slash_commands_markdown()
        
        assert len(all_md) == 9
        for workflow in TemplateManager.WORKFLOWS:
            assert workflow in all_md


class TestToolRegistry:
    """Tests for tool registry."""
    
    def test_registry_populated(self):
        """Test that registry is populated with all tools."""
        # Should have 20 tools registered
        assert ToolRegistry.get_count() >= 20
    
    def test_get_tool(self):
        """Test getting a tool by slug."""
        claude = ToolRegistry.get("claude")
        assert claude is not None
        assert claude.name == "Claude Code"
        assert claude.slug == "claude"
    
    def test_get_nonexistent_tool(self):
        """Test getting a tool that doesn't exist."""
        tool = ToolRegistry.get("nonexistent")
        assert tool is None
    
    def test_list_all(self):
        """Test listing all tools."""
        all_tools = ToolRegistry.list_all()
        assert len(all_tools) >= 20
        
        # Check some known tools
        slugs = [t.slug for t in all_tools]
        assert "claude" in slugs
        assert "cursor" in slugs
        assert "windsurf" in slugs
        assert "copilot" in slugs
    
    def test_list_by_priority(self):
        """Test listing tools by priority."""
        high_tools = ToolRegistry.list_by_priority("high")
        medium_tools = ToolRegistry.list_by_priority("medium")
        low_tools = ToolRegistry.list_by_priority("low")
        
        assert len(high_tools) > 0
        assert len(medium_tools) > 0
        assert len(low_tools) > 0
        
        # Verify priority is correct
        for tool in high_tools:
            assert tool.priority == "high"
    
    def test_list_by_type(self):
        """Test listing tools by integration type."""
        root_only = ToolRegistry.list_by_type("root_only")
        slash_only = ToolRegistry.list_by_type("slash_only")
        hybrid = ToolRegistry.list_by_type("hybrid")
        
        assert len(root_only) > 0
        assert len(slash_only) > 0
        assert len(hybrid) > 0
    
    def test_get_summary(self):
        """Test getting registry summary."""
        summary = ToolRegistry.get_summary()
        
        assert "total" in summary
        assert "high_priority" in summary
        assert "medium_priority" in summary
        assert "low_priority" in summary
        assert "root_only" in summary
        assert "slash_only" in summary
        assert "hybrid" in summary
        
        # Verify counts add up
        priority_total = (summary["high_priority"] + 
                         summary["medium_priority"] + 
                         summary["low_priority"])
        assert priority_total == summary["total"]


class TestClaudeConfigurator:
    """Tests for Claude Code configurator."""
    
    def test_properties(self):
        """Test configurator properties."""
        claude = ClaudeConfigurator()
        
        assert claude.name == "Claude Code"
        assert claude.slug == "claude"
        assert claude.config_file_name == "CLAUDE.md"
        assert claude.slash_command_dir == ".claude/prompts"
        assert claude.command_format == "toml"
        assert claude.priority == "high"
        assert claude.integration_type == "hybrid"
    
    def test_configure(self, tmp_path):
        """Test configuring Claude integration."""
        claude = ClaudeConfigurator()
        result = claude.configure(tmp_path)
        
        assert result.success
        assert len(result.messages) > 0
        assert len(result.files_created) == 10  # 1 root + 9 commands
        
        # Verify root config exists
        root_config = tmp_path / "CLAUDE.md"
        assert root_config.exists()
        
        content = root_config.read_text()
        assert "<!-- STRIDE:START -->" in content
        assert "/stride:init" in content
        
        # Verify slash commands exist
        slash_dir = tmp_path / ".claude" / "prompts"
        assert slash_dir.exists()
        
        for workflow in TemplateManager.WORKFLOWS:
            command_file = slash_dir / f"stride-{workflow}.toml"
            assert command_file.exists()
            
            content = command_file.read_text()
            assert "# STRIDE:START" in content
            assert f'name = "stride-{workflow}"' in content
    
    def test_validate_success(self, tmp_path):
        """Test validation of correct Claude integration."""
        claude = ClaudeConfigurator()
        claude.configure(tmp_path)
        
        validation = claude.validate(tmp_path)
        assert validation.valid
        assert len(validation.issues) == 0
    
    def test_validate_missing_files(self, tmp_path):
        """Test validation with missing files."""
        claude = ClaudeConfigurator()
        validation = claude.validate(tmp_path)
        
        assert not validation.valid
        assert len(validation.issues) > 0
    
    def test_update(self, tmp_path):
        """Test updating Claude integration."""
        claude = ClaudeConfigurator()
        
        # Initial configure
        claude.configure(tmp_path)
        
        # Add custom content
        root_config = tmp_path / "CLAUDE.md"
        original_content = root_config.read_text()
        custom_content = original_content + "\n\n# My Custom Section\n\nCustom instructions here\n"
        root_config.write_text(custom_content)
        
        # Update
        result = claude.update(tmp_path)
        assert result.success
        
        # Verify custom content preserved
        updated_content = root_config.read_text()
        assert "# My Custom Section" in updated_content
        assert "<!-- STRIDE:START -->" in updated_content


class TestWindsurfConfigurator:
    """Tests for Windsurf configurator."""
    
    def test_properties(self):
        """Test configurator properties."""
        windsurf = WindsurfConfigurator()
        
        assert windsurf.name == "Windsurf"
        assert windsurf.slug == "windsurf"
        assert windsurf.config_file_name is None
        assert windsurf.slash_command_dir == ".windsurf/workflows"
        assert windsurf.command_format == "markdown"
        assert windsurf.priority == "high"
        assert windsurf.integration_type == "slash_only"
    
    def test_configure(self, tmp_path):
        """Test configuring Windsurf integration."""
        windsurf = WindsurfConfigurator()
        result = windsurf.configure(tmp_path)
        
        assert result.success
        assert len(result.files_created) == 9  # 9 workflow files
        
        # Verify workflow files exist
        workflows_dir = tmp_path / ".windsurf" / "workflows"
        assert workflows_dir.exists()
        
        for workflow in TemplateManager.WORKFLOWS:
            workflow_file = workflows_dir / f"stride-{workflow}.md"
            assert workflow_file.exists()
            
            content = workflow_file.read_text()
            assert "---" in content  # YAML frontmatter
            assert "<!-- STRIDE:START -->" in content
            assert "auto_execution_mode:" in content


class TestClineConfigurator:
    """Tests for Cline configurator."""
    
    def test_properties(self):
        """Test configurator properties."""
        cline = ClineConfigurator()
        
        assert cline.name == "Cline"
        assert cline.slug == "cline"
        assert cline.config_file_name == "CLINE.md"
        assert cline.slash_command_dir is None
        assert cline.command_format is None
        assert cline.priority == "high"
        assert cline.integration_type == "root_only"
    
    def test_configure(self, tmp_path):
        """Test configuring Cline integration."""
        cline = ClineConfigurator()
        result = cline.configure(tmp_path)
        
        assert result.success
        assert len(result.files_created) == 1  # Just root config
        
        # Verify root config exists
        root_config = tmp_path / "CLINE.md"
        assert root_config.exists()
        
        content = root_config.read_text()
        assert "<!-- STRIDE:START -->" in content
        assert "# Stride Sprint Management" in content


class TestIntegration:
    """Integration tests."""
    
    def test_configure_all_high_priority_tools(self, tmp_path):
        """Test configuring all high-priority tools."""
        high_tools = ToolRegistry.list_by_priority("high")
        
        for tool in high_tools:
            result = tool.configure(tmp_path)
            assert result.success, f"Failed to configure {tool.name}"
            
            # Validate immediately
            validation = tool.validate(tmp_path)
            assert validation.valid, f"Validation failed for {tool.name}: {validation.issues}"
    
    def test_universal_agents_md_created(self, tmp_path):
        """Test that universal AGENTS.md is created."""
        universal = ToolRegistry.get("universal")
        assert universal is not None
        
        result = universal.configure(tmp_path)
        assert result.success
        
        agents_md = tmp_path / "stride" / "AGENTS.md"
        assert agents_md.exists()
        
        content = agents_md.read_text()
        assert len(content) > 500
        assert "# Stride AI Agent Integration Guide" in content
    
    def test_all_tools_have_unique_slugs(self):
        """Test that all tools have unique slugs."""
        all_tools = ToolRegistry.list_all()
        slugs = [t.slug for t in all_tools]
        
        assert len(slugs) == len(set(slugs)), "Duplicate slugs found"
    
    def test_all_tools_can_configure(self, tmp_path):
        """Test that all tools can configure without errors."""
        all_tools = ToolRegistry.list_all()
        
        for tool in all_tools:
            result = tool.configure(tmp_path)
            assert result.success, f"Tool {tool.name} failed to configure: {result.messages}"
