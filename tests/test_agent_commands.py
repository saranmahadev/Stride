"""
Tests for agent CLI commands.
"""
import shutil
import tempfile
from pathlib import Path
import pytest
import json
from click.testing import CliRunner
from stride.cli.main import cli
from stride.core.config_manager import ConfigManager


@pytest.fixture
def temp_project(monkeypatch):
    """Create temporary project directory and isolate config."""
    tmp = Path(tempfile.mkdtemp())
    # Change to temp directory to isolate config files
    monkeypatch.chdir(tmp)
    yield tmp
    shutil.rmtree(tmp, ignore_errors=True)


class TestAgentListCommand:
    """Tests for 'stride agent list' command."""
    
    def test_agent_list_no_configured(self, temp_project):
        """Test listing agents when none are configured."""
        runner = CliRunner()
        result = runner.invoke(cli, ['agent', 'list'])
        
        assert result.exit_code == 0
        assert '🤖 AI Agents' in result.output
        assert '0 configured' in result.output
        assert 'Claude' in result.output
        assert 'Copilot' in result.output
        assert '·' in result.output  # All should show · (not configured)
    
    def test_agent_list_with_configured(self, temp_project):
        """Test listing agents when some are configured."""
        # Add an agent first
        cm = ConfigManager()
        cm.add_agent('claude')
        
        runner = CliRunner()
        result = runner.invoke(cli, ['agent', 'list'])
        
        assert result.exit_code == 0
        assert '1 configured' in result.output
        assert '✓' in result.output  # Claude should show ✓
    
    def test_agent_list_json_output(self, temp_project):
        """Test JSON output format."""
        runner = CliRunner()
        result = runner.invoke(cli, ['agent', 'list', '--json'])
        
        assert result.exit_code == 0
        
        data = json.loads(result.output)
        assert 'configured_count' in data
        assert 'available_count' in data
        assert 'agents' in data
        assert isinstance(data['agents'], list)
        assert len(data['agents']) == 7  # 7 agents in registry
        
        # Check structure of first agent
        agent = data['agents'][0]
        assert 'id' in agent
        assert 'name' in agent
        assert 'description' in agent
        assert 'configured' in agent
        assert isinstance(agent['configured'], bool)


class TestAgentAddCommand:
    """Tests for 'stride agent add' command."""
    
    def test_agent_add_valid(self, temp_project):
        """Test adding a valid agent."""
        runner = CliRunner()
        result = runner.invoke(cli, ['agent', 'add', 'claude'])
        
        assert result.exit_code == 0
        assert '✅ Added agent: Claude' in result.output
        assert 'Total configured agents: 1' in result.output
        
        # Verify it was added
        cm = ConfigManager()
        assert 'claude' in cm.get_agents()
    
    def test_agent_add_invalid(self, temp_project):
        """Test adding an invalid agent ID."""
        runner = CliRunner()
        result = runner.invoke(cli, ['agent', 'add', 'invalid_agent'])
        
        assert result.exit_code == 1
        assert '❌ Invalid agent ID' in result.output
        assert 'Available agents:' in result.output
    
    def test_agent_add_already_configured(self, temp_project):
        """Test adding an agent that's already configured."""
        # Add agent first
        cm = ConfigManager()
        cm.add_agent('claude')
        
        runner = CliRunner()
        result = runner.invoke(cli, ['agent', 'add', 'claude'])
        
        assert result.exit_code == 0
        assert 'Already configured' in result.output
    
    def test_agent_add_quiet_mode(self, temp_project):
        """Test adding agent in quiet mode."""
        runner = CliRunner()
        result = runner.invoke(cli, ['agent', 'add', 'claude', '--quiet'])
        
        assert result.exit_code == 0
        assert result.output.strip() == ''  # No output in quiet mode
        
        # Verify it was added
        cm = ConfigManager()
        assert 'claude' in cm.get_agents()
    
    def test_agent_add_case_insensitive(self, temp_project):
        """Test that agent IDs are case-insensitive."""
        runner = CliRunner()
        result = runner.invoke(cli, ['agent', 'add', 'CLAUDE'])
        
        assert result.exit_code == 0
        
        # Verify it was added as lowercase
        cm = ConfigManager()
        agents = cm.get_agents()
        assert 'claude' in agents


class TestAgentRemoveCommand:
    """Tests for 'stride agent remove' command."""
    
    def test_agent_remove_configured(self, temp_project):
        """Test removing a configured agent."""
        # Add agent first
        cm = ConfigManager()
        cm.add_agent('claude')
        cm.add_agent('copilot')
        
        runner = CliRunner()
        result = runner.invoke(cli, ['agent', 'remove', 'claude'])
        
        assert result.exit_code == 0
        assert '✅ Removed agent: Claude' in result.output
        assert 'Remaining agents: 1' in result.output
        
        # Verify it was removed
        agents = cm.get_agents()
        assert 'claude' not in agents
        assert 'copilot' in agents
    
    def test_agent_remove_not_configured(self, temp_project):
        """Test removing an agent that's not configured."""
        runner = CliRunner()
        result = runner.invoke(cli, ['agent', 'remove', 'claude'])
        
        assert result.exit_code == 0
        assert 'not configured' in result.output.lower()
    
    def test_agent_remove_quiet_mode(self, temp_project):
        """Test removing agent in quiet mode."""
        # Add agent first
        cm = ConfigManager()
        cm.add_agent('claude')
        
        runner = CliRunner()
        result = runner.invoke(cli, ['agent', 'remove', 'claude', '--quiet'])
        
        assert result.exit_code == 0
        assert result.output.strip() == ''
        
        # Verify it was removed
        assert 'claude' not in cm.get_agents()


class TestAgentInfoCommand:
    """Tests for 'stride agent info' command."""
    
    def test_agent_info_valid_configured(self, temp_project):
        """Test showing info for a configured agent."""
        # Add agent first
        cm = ConfigManager()
        cm.add_agent('claude')
        
        runner = CliRunner()
        result = runner.invoke(cli, ['agent', 'info', 'claude'])
        
        assert result.exit_code == 0
        assert '🤖 Claude' in result.output
        assert 'ID: claude' in result.output
        assert 'Description:' in result.output
        assert 'Website:' in result.output
        assert 'Configured: ✓ Yes' in result.output
        assert 'Remove with:' in result.output
    
    def test_agent_info_valid_not_configured(self, temp_project):
        """Test showing info for a valid but not configured agent."""
        runner = CliRunner()
        result = runner.invoke(cli, ['agent', 'info', 'copilot'])
        
        assert result.exit_code == 0
        assert '🤖 GitHub Copilot' in result.output
        assert 'Configured: ✗ No' in result.output
        assert 'Add to project with:' in result.output
    
    def test_agent_info_invalid(self, temp_project):
        """Test showing info for an invalid agent."""
        runner = CliRunner()
        result = runner.invoke(cli, ['agent', 'info', 'invalid_agent'])
        
        assert result.exit_code == 1
        assert '❌ Unknown agent' in result.output
        assert 'Available agents:' in result.output
    
    def test_agent_info_case_insensitive(self, temp_project):
        """Test that agent info is case-insensitive."""
        runner = CliRunner()
        result = runner.invoke(cli, ['agent', 'info', 'CLAUDE'])
        
        assert result.exit_code == 0
        assert 'Claude' in result.output


class TestAgentCommandHelp:
    """Tests for agent command help text."""
    
    def test_agent_group_help(self):
        """Test agent group help text."""
        runner = CliRunner()
        result = runner.invoke(cli, ['agent', '--help'])
        
        assert result.exit_code == 0
        assert 'Manage AI agents' in result.output
        assert 'list' in result.output
        assert 'add' in result.output
        assert 'remove' in result.output
        assert 'info' in result.output
    
    def test_agent_list_help(self):
        """Test agent list help text."""
        runner = CliRunner()
        result = runner.invoke(cli, ['agent', 'list', '--help'])
        
        assert result.exit_code == 0
        assert 'List all available AI agents' in result.output
        assert '--json' in result.output
    
    def test_agent_add_help(self):
        """Test agent add help text."""
        runner = CliRunner()
        result = runner.invoke(cli, ['agent', 'add', '--help'])
        
        assert result.exit_code == 0
        assert 'Add' in result.output
        assert 'agent' in result.output.lower()
        assert '--quiet' in result.output
    
    def test_agent_remove_help(self):
        """Test agent remove help text."""
        runner = CliRunner()
        result = runner.invoke(cli, ['agent', 'remove', '--help'])
        
        assert result.exit_code == 0
        assert 'Remove' in result.output
        assert '--quiet' in result.output
    
    def test_agent_info_help(self):
        """Test agent info help text."""
        runner = CliRunner()
        result = runner.invoke(cli, ['agent', 'info', '--help'])
        
        assert result.exit_code == 0
        assert 'Show detailed information' in result.output


class TestAgentIntegration:
    """Integration tests for agent commands."""
    
    def test_full_agent_workflow(self, temp_project):
        """Test complete workflow: list -> add -> info -> remove -> list."""
        runner = CliRunner()
        
        # 1. List (should be empty)
        result = runner.invoke(cli, ['agent', 'list'])
        assert '0 configured' in result.output
        
        # 2. Add agent
        result = runner.invoke(cli, ['agent', 'add', 'claude'])
        assert result.exit_code == 0
        assert '✅ Added' in result.output
        
        # 3. Check info
        result = runner.invoke(cli, ['agent', 'info', 'claude'])
        assert result.exit_code == 0
        assert 'Configured: ✓ Yes' in result.output
        
        # 4. List again (should show 1 configured)
        result = runner.invoke(cli, ['agent', 'list'])
        assert '1 configured' in result.output
        assert '✓' in result.output
        
        # 5. Remove agent
        result = runner.invoke(cli, ['agent', 'remove', 'claude'])
        assert result.exit_code == 0
        assert '✅ Removed' in result.output
        
        # 6. List final (should be empty again)
        result = runner.invoke(cli, ['agent', 'list'])
        assert '0 configured' in result.output
    
    def test_add_multiple_agents_sequentially(self, temp_project):
        """Test adding multiple agents one by one."""
        runner = CliRunner()
        
        # Add first agent
        result = runner.invoke(cli, ['agent', 'add', 'claude'])
        assert result.exit_code == 0
        
        # Add second agent
        result = runner.invoke(cli, ['agent', 'add', 'copilot'])
        assert result.exit_code == 0
        
        # Verify both are configured
        cm = ConfigManager()
        agents = cm.get_agents()
        assert 'claude' in agents
        assert 'copilot' in agents
        assert len(agents) == 2
        
        # List should show 2 configured
        result = runner.invoke(cli, ['agent', 'list'])
        assert '2 configured' in result.output
