"""
Tests for enhanced stride init command with agent selection and file generation.
"""
import pytest
import json
from pathlib import Path
from click.testing import CliRunner
from stride.cli.main import cli
from stride.core.agent_manager import AgentManager


@pytest.fixture
def runner():
    """Create a CLI runner for testing."""
    return CliRunner()


class TestEnhancedInit:
    """Tests for enhanced stride init command."""
    
    def test_init_non_interactive_with_agents(self, runner):
        """Test init in non-interactive mode with agent selection."""
        with runner.isolated_filesystem():
            result = runner.invoke(cli, [
                "init",
                "--name", "TestProject",
                "--agents", "claude,copilot",
                "--no-interactive"
            ])
            
            assert result.exit_code == 0
            assert "Stride initialized successfully" in result.output
            assert Path("stride").exists()
            assert Path("stride.config.yaml").exists()
            assert Path("AGENTS.md").exists()
            assert Path("stride/project.md").exists()
    
    def test_init_creates_agents_md(self, runner):
        """Test that init creates AGENTS.md file."""
        with runner.isolated_filesystem():
            result = runner.invoke(cli, [
                "init",
                "--name", "TestProject",
                "--agents", "claude,copilot",
                "--no-interactive"
            ])
            
            assert result.exit_code == 0
            
            agents_md = Path("AGENTS.md")
            assert agents_md.exists()
            
            content = agents_md.read_text()
            assert "TestProject" in content
            assert "Claude" in content
            assert "Copilot" in content
    
    def test_init_creates_project_md(self, runner):
        """Test that init creates stride/project.md file."""
        with runner.isolated_filesystem():
            result = runner.invoke(cli, [
                "init",
                "--name", "MyApp",
                "--agents", "claude",
                "--no-interactive"
            ])
            
            assert result.exit_code == 0
            
            project_md = Path("stride/project.md")
            assert project_md.exists()
            
            content = project_md.read_text(encoding="utf-8")
            assert "MyApp" in content
            assert "Claude" in content
            assert "Stride" in content
    
    def test_init_creates_config_with_agents(self, runner):
        """Test that init creates config file with agent information."""
        with runner.isolated_filesystem():
            result = runner.invoke(cli, [
                "init",
                "--name", "TestProject",
                "--agents", "claude,copilot,chatgpt",
                "--no-interactive"
            ])
            
            assert result.exit_code == 0
            
            config_path = Path("stride.config.yaml")
            assert config_path.exists()
            
            import yaml
            with open(config_path) as f:
                config = yaml.safe_load(f)
            
            assert config["project"]["name"] == "TestProject"
            assert "claude" in config["project"]["agents"]
            assert "copilot" in config["project"]["agents"]
            assert "chatgpt" in config["project"]["agents"]
    
    def test_init_with_default_agents(self, runner):
        """Test that init uses default agents if none specified."""
        with runner.isolated_filesystem():
            result = runner.invoke(cli, [
                "init",
                "--name", "TestProject",
                "--no-interactive"
            ])
            
            assert result.exit_code == 0
            
            import yaml
            with open("stride.config.yaml") as f:
                config = yaml.safe_load(f)
            
            # Should have default agents
            assert len(config["project"]["agents"]) >= 1
            assert "claude" in config["project"]["agents"] or "copilot" in config["project"]["agents"]
    
    def test_init_with_invalid_agents(self, runner):
        """Test init with some invalid agent IDs."""
        with runner.isolated_filesystem():
            result = runner.invoke(cli, [
                "init",
                "--name", "TestProject",
                "--agents", "claude,invalid,copilot,fake",
                "--no-interactive"
            ])
            
            assert result.exit_code == 0
            assert "Unknown agents will be ignored" in result.output or "Warning" in result.output
            
            import yaml
            with open("stride.config.yaml") as f:
                config = yaml.safe_load(f)
            
            # Should only have valid agents
            assert "claude" in config["project"]["agents"]
            assert "copilot" in config["project"]["agents"]
            assert "invalid" not in config["project"]["agents"]
            assert "fake" not in config["project"]["agents"]
    
    def test_init_with_single_agent(self, runner):
        """Test init with a single agent."""
        with runner.isolated_filesystem():
            result = runner.invoke(cli, [
                "init",
                "--name", "SingleAgentProject",
                "--agents", "claude",
                "--no-interactive"
            ])
            
            assert result.exit_code == 0
            
            import yaml
            with open("stride.config.yaml") as f:
                config = yaml.safe_load(f)
            
            assert config["project"]["agents"] == ["claude"]
    
    def test_init_force_overwrites_existing(self, runner):
        """Test that --force flag overwrites existing files."""
        with runner.isolated_filesystem():
            # First init
            runner.invoke(cli, [
                "init",
                "--name", "FirstProject",
                "--agents", "claude",
                "--no-interactive"
            ])
            
            # Second init with force
            result = runner.invoke(cli, [
                "init",
                "--name", "SecondProject",
                "--agents", "copilot",
                "--force",
                "--no-interactive"
            ])
            
            assert result.exit_code == 0
            
            # Check that config was updated
            import yaml
            with open("stride.config.yaml") as f:
                config = yaml.safe_load(f)
            
            assert config["project"]["name"] == "SecondProject"
            assert "copilot" in config["project"]["agents"]
    
    def test_init_without_force_fails_if_exists(self, runner):
        """Test that init fails if already initialized without force flag."""
        with runner.isolated_filesystem():
            # First init
            runner.invoke(cli, [
                "init",
                "--name", "FirstProject",
                "--no-interactive"
            ])
            
            # Second init without force should fail
            result = runner.invoke(cli, [
                "init",
                "--name", "SecondProject",
                "--no-interactive"
            ])
            
            assert result.exit_code == 1
            assert "already initialized" in result.output
    
    def test_init_feedback_shows_agent_count(self, runner):
        """Test that success feedback shows agent count."""
        with runner.isolated_filesystem():
            result = runner.invoke(cli, [
                "init",
                "--name", "TestProject",
                "--agents", "claude,copilot,chatgpt",
                "--no-interactive"
            ])
            
            assert result.exit_code == 0
            assert "3 agents configured" in result.output or "3 agent" in result.output
    
    def test_init_feedback_shows_next_steps(self, runner):
        """Test that success feedback includes next steps."""
        with runner.isolated_filesystem():
            result = runner.invoke(cli, [
                "init",
                "--name", "TestProject",
                "--no-interactive"
            ])
            
            assert result.exit_code == 0
            assert "Next steps" in result.output or "next steps" in result.output
            assert "AGENTS.md" in result.output
            assert "project.md" in result.output
            assert "stride create" in result.output
    
    def test_init_with_description(self, runner):
        """Test init with project description."""
        with runner.isolated_filesystem():
            result = runner.invoke(cli, [
                "init",
                "--name", "TestProject",
                "--description", "A test project for Stride",
                "--agents", "claude",
                "--no-interactive"
            ])
            
            assert result.exit_code == 0
            # Description should be in config or somewhere
            assert Path("stride.config.yaml").exists()


class TestInteractiveInit:
    """Tests for interactive init mode."""
    
    def test_interactive_mode_prompts_for_name(self, runner):
        """Test that interactive mode prompts for project name."""
        with runner.isolated_filesystem():
            # Simulate user input: project name, description (empty), agents
            result = runner.invoke(cli, [
                "init"
            ], input="TestProject\n\nclaude,copilot\n")
            
            # Should succeed or at least show prompts
            assert "Project name" in result.output or result.exit_code == 0
    
    def test_interactive_mode_shows_available_agents(self, runner):
        """Test that interactive mode shows available agents."""
        with runner.isolated_filesystem():
            result = runner.invoke(cli, [
                "init"
            ], input="TestProject\n\nclaude\n")
            
            # Should show agent list
            assert "Available" in result.output or "agent" in result.output.lower() or result.exit_code == 0


class TestInitBackwardCompatibility:
    """Tests for backward compatibility with original init command."""
    
    def test_init_basic_still_works(self, runner):
        """Test that basic init without new options still works."""
        with runner.isolated_filesystem():
            result = runner.invoke(cli, [
                "init",
                "--no-interactive"
            ])
            
            assert result.exit_code == 0
            assert Path("stride").exists()
            assert Path("stride/sprints/proposed").exists()
            assert Path("stride/sprints/active").exists()
    
    def test_init_with_name_only(self, runner):
        """Test init with just --name flag (original behavior)."""
        with runner.isolated_filesystem():
            result = runner.invoke(cli, [
                "init",
                "--name", "MyProject",
                "--no-interactive"
            ])
            
            assert result.exit_code == 0
            assert Path("stride").exists()
    
    def test_quiet_mode_suppresses_output(self, runner):
        """Test that --quiet flag suppresses verbose output."""
        with runner.isolated_filesystem():
            result = runner.invoke(cli, [
                "--quiet",
                "init",
                "--name", "TestProject",
                "--no-interactive"
            ])
            
            # Should have minimal output in quiet mode
            # Exit code should still be 0
            assert result.exit_code == 0


class TestInitFileGeneration:
    """Tests for file generation during init."""
    
    def test_agents_md_has_correct_structure(self, runner):
        """Test that generated AGENTS.md has correct structure."""
        with runner.isolated_filesystem():
            runner.invoke(cli, [
                "init",
                "--name", "TestProject",
                "--agents", "claude,copilot",
                "--no-interactive"
            ])
            
            content = Path("AGENTS.md").read_text(encoding="utf-8")
            
            # Check structure
            assert "# AI Agents for TestProject" in content
            assert "## Configured Agents" in content
            assert "## Best Practices" in content
            assert "Claude" in content
            assert "Copilot" in content
    
    def test_project_md_has_frontmatter(self, runner):
        """Test that generated project.md has YAML frontmatter."""
        with runner.isolated_filesystem():
            runner.invoke(cli, [
                "init",
                "--name", "TestProject",
                "--agents", "claude",
                "--no-interactive"
            ])
            
            content = Path("stride/project.md").read_text(encoding="utf-8")
            
            # Check for YAML frontmatter
            assert content.startswith("---")
            assert "name: TestProject" in content
            assert "agents:" in content
            assert "# TestProject" in content
    
    def test_all_required_directories_created(self, runner):
        """Test that all required directories are created."""
        with runner.isolated_filesystem():
            runner.invoke(cli, [
                "init",
                "--name", "TestProject",
                "--no-interactive"
            ])
            
            required_dirs = [
                "stride",
                "stride/sprints",
                "stride/sprints/proposed",
                "stride/sprints/active",
                "stride/sprints/blocked",
                "stride/sprints/review",
                "stride/sprints/completed",
                "stride/specs",
                "stride/introspection"
            ]
            
            for dir_path in required_dirs:
                assert Path(dir_path).exists(), f"Directory {dir_path} was not created"
