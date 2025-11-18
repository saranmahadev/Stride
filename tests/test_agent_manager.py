"""
Tests for AgentManager - AI Agent Registry and Management.
"""
import pytest
from stride.core.agent_manager import AgentManager, Agent


class TestAgentRegistry:
    """Tests for agent registry functionality."""
    
    def test_all_default_agents_exist(self):
        """Test that all expected default agents are in the registry."""
        expected_agents = ["claude", "copilot", "chatgpt", "gemini", "cursor", "windsurf", "custom"]
        actual_ids = AgentManager.get_agent_ids()
        
        for expected in expected_agents:
            assert expected in actual_ids, f"Expected agent '{expected}' not found in registry"
    
    def test_get_agent_valid(self):
        """Test getting a valid agent by ID."""
        agent = AgentManager.get_agent("claude")
        
        assert agent is not None
        assert agent.id == "claude"
        assert agent.name == "Claude (Anthropic)"
        assert agent.description
        assert agent.primary_use
        assert agent.access_method
    
    def test_get_agent_case_insensitive(self):
        """Test that agent lookup is case-insensitive."""
        agent1 = AgentManager.get_agent("claude")
        agent2 = AgentManager.get_agent("CLAUDE")
        agent3 = AgentManager.get_agent("Claude")
        
        assert agent1 == agent2 == agent3
    
    def test_get_agent_invalid(self):
        """Test getting an invalid agent returns None."""
        agent = AgentManager.get_agent("nonexistent")
        assert agent is None
    
    def test_get_all_agents(self):
        """Test getting all agents returns a list of Agent objects."""
        agents = AgentManager.get_all_agents()
        
        assert isinstance(agents, list)
        assert len(agents) >= 7  # At least our default agents
        assert all(isinstance(agent, Agent) for agent in agents)
    
    def test_get_agent_ids(self):
        """Test getting all agent IDs."""
        ids = AgentManager.get_agent_ids()
        
        assert isinstance(ids, list)
        assert "claude" in ids
        assert "copilot" in ids
        assert "chatgpt" in ids


class TestAgentValidation:
    """Tests for agent ID validation."""
    
    def test_validate_all_valid(self):
        """Test validating a list of all valid agent IDs."""
        valid, invalid = AgentManager.validate_agent_ids(["claude", "copilot", "chatgpt"])
        
        assert len(valid) == 3
        assert len(invalid) == 0
        assert "claude" in valid
        assert "copilot" in valid
        assert "chatgpt" in valid
    
    def test_validate_all_invalid(self):
        """Test validating a list of all invalid agent IDs."""
        valid, invalid = AgentManager.validate_agent_ids(["fake1", "fake2", "fake3"])
        
        assert len(valid) == 0
        assert len(invalid) == 3
        assert "fake1" in invalid
        assert "fake2" in invalid
    
    def test_validate_mixed(self):
        """Test validating a mix of valid and invalid agent IDs."""
        valid, invalid = AgentManager.validate_agent_ids(["claude", "fake", "copilot", "invalid"])
        
        assert len(valid) == 2
        assert len(invalid) == 2
        assert "claude" in valid
        assert "copilot" in valid
        assert "fake" in invalid
        assert "invalid" in invalid
    
    def test_validate_empty_list(self):
        """Test validating an empty list."""
        valid, invalid = AgentManager.validate_agent_ids([])
        
        assert len(valid) == 0
        assert len(invalid) == 0
    
    def test_validate_case_insensitive(self):
        """Test that validation is case-insensitive."""
        valid, invalid = AgentManager.validate_agent_ids(["CLAUDE", "CoPilot", "chatgpt"])
        
        assert len(valid) == 3
        assert len(invalid) == 0


class TestAgentParsing:
    """Tests for agent string parsing."""
    
    def test_parse_simple_string(self):
        """Test parsing a simple comma-separated string."""
        result = AgentManager.parse_agent_string("claude,copilot,chatgpt")
        
        assert result == ["claude", "copilot", "chatgpt"]
    
    def test_parse_with_spaces(self):
        """Test parsing a string with spaces around commas."""
        result = AgentManager.parse_agent_string("claude, copilot , chatgpt")
        
        assert result == ["claude", "copilot", "chatgpt"]
    
    def test_parse_mixed_case(self):
        """Test that parsing normalizes to lowercase."""
        result = AgentManager.parse_agent_string("CLAUDE,CoPilot,ChatGPT")
        
        assert result == ["claude", "copilot", "chatgpt"]
    
    def test_parse_empty_string(self):
        """Test parsing an empty string."""
        result = AgentManager.parse_agent_string("")
        
        assert result == []
    
    def test_parse_whitespace_only(self):
        """Test parsing a string with only whitespace."""
        result = AgentManager.parse_agent_string("   ")
        
        assert result == []
    
    def test_parse_single_agent(self):
        """Test parsing a single agent."""
        result = AgentManager.parse_agent_string("claude")
        
        assert result == ["claude"]
    
    def test_parse_trailing_comma(self):
        """Test parsing a string with trailing comma."""
        result = AgentManager.parse_agent_string("claude,copilot,")
        
        assert result == ["claude", "copilot"]


class TestAgentDisplay:
    """Tests for agent display functionality."""
    
    def test_get_agent_choices_text(self):
        """Test getting formatted agent choices text."""
        text = AgentManager.get_agent_choices_text()
        
        assert "Available agents:" in text
        assert "Claude" in text
        assert "Copilot" in text
        assert "ChatGPT" in text
    
    def test_get_agent_display_name_valid(self):
        """Test getting display name for a valid agent."""
        name = AgentManager.get_agent_display_name("claude")
        
        assert name == "Claude (Anthropic)"
    
    def test_get_agent_display_name_invalid(self):
        """Test getting display name for an invalid agent returns the ID."""
        name = AgentManager.get_agent_display_name("nonexistent")
        
        assert name == "nonexistent"
    
    def test_get_agent_display_name_case_insensitive(self):
        """Test that display name lookup is case-insensitive."""
        name1 = AgentManager.get_agent_display_name("claude")
        name2 = AgentManager.get_agent_display_name("CLAUDE")
        
        assert name1 == name2


class TestAgentDataClass:
    """Tests for the Agent dataclass."""
    
    def test_agent_creation(self):
        """Test creating an Agent instance."""
        agent = Agent(
            id="test",
            name="Test Agent",
            description="A test agent",
            primary_use="Testing",
            access_method="Test access"
        )
        
        assert agent.id == "test"
        assert agent.name == "Test Agent"
        assert agent.description == "A test agent"
        assert agent.primary_use == "Testing"
        assert agent.access_method == "Test access"
        assert agent.website is None
    
    def test_agent_with_website(self):
        """Test creating an Agent with a website."""
        agent = Agent(
            id="test",
            name="Test Agent",
            description="A test agent",
            primary_use="Testing",
            access_method="Test access",
            website="https://test.com"
        )
        
        assert agent.website == "https://test.com"
    
    def test_agent_equality(self):
        """Test that agents with same data are equal."""
        agent1 = Agent(
            id="test",
            name="Test Agent",
            description="A test agent",
            primary_use="Testing",
            access_method="Test access"
        )
        agent2 = Agent(
            id="test",
            name="Test Agent",
            description="A test agent",
            primary_use="Testing",
            access_method="Test access"
        )
        
        assert agent1 == agent2


class TestSpecificAgents:
    """Tests for specific agents in the registry."""
    
    def test_claude_agent(self):
        """Test Claude agent has correct properties."""
        agent = AgentManager.get_agent("claude")
        
        assert agent.id == "claude"
        assert "Anthropic" in agent.name
        assert agent.website == "https://claude.ai"
    
    def test_copilot_agent(self):
        """Test GitHub Copilot agent has correct properties."""
        agent = AgentManager.get_agent("copilot")
        
        assert agent.id == "copilot"
        assert "GitHub" in agent.name or "Copilot" in agent.name
        assert "copilot" in agent.website
    
    def test_custom_agent(self):
        """Test custom agent exists for user-defined tools."""
        agent = AgentManager.get_agent("custom")
        
        assert agent.id == "custom"
        assert "Custom" in agent.name
        assert agent.website is None
