"""
Agent Manager - AI Agent Registry and Management.

This module manages the registry of available AI agents and provides
functionality for agent selection and configuration.
"""
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class Agent:
    """Represents an AI agent configuration."""
    id: str
    name: str
    description: str
    primary_use: str
    access_method: str
    website: Optional[str] = None


class AgentManager:
    """Manages AI agent registry and selection."""
    
    # Registry of available AI agents
    AGENTS: Dict[str, Agent] = {
        "claude": Agent(
            id="claude",
            name="Claude (Anthropic)",
            description="Advanced AI with strong reasoning, coding, and analysis capabilities",
            primary_use="Complex problem-solving, code architecture, detailed technical discussions",
            access_method="claude.ai, API, or IDE extensions",
            website="https://claude.ai"
        ),
        "copilot": Agent(
            id="copilot",
            name="GitHub Copilot",
            description="AI pair programmer integrated directly into your IDE",
            primary_use="Real-time code completion, inline suggestions, code generation",
            access_method="VS Code, JetBrains IDEs, Neovim, and other supported editors",
            website="https://github.com/features/copilot"
        ),
        "chatgpt": Agent(
            id="chatgpt",
            name="ChatGPT (OpenAI)",
            description="Versatile conversational AI for general tasks and coding",
            primary_use="Brainstorming, explanations, quick coding tasks, documentation",
            access_method="chat.openai.com or API",
            website="https://chat.openai.com"
        ),
        "gemini": Agent(
            id="gemini",
            name="Gemini (Google)",
            description="Multimodal AI model with strong analytical capabilities",
            primary_use="Data analysis, multi-modal tasks, research, code review",
            access_method="gemini.google.com or Google AI Studio",
            website="https://gemini.google.com"
        ),
        "cursor": Agent(
            id="cursor",
            name="Cursor AI",
            description="AI-first code editor with advanced context awareness",
            primary_use="Full-project context coding, multi-file edits, codebase understanding",
            access_method="Cursor desktop application",
            website="https://cursor.sh"
        ),
        "windsurf": Agent(
            id="windsurf",
            name="Windsurf (Codeium)",
            description="AI-powered IDE with agentic flow capabilities",
            primary_use="Autonomous coding tasks, multi-step implementations, refactoring",
            access_method="Windsurf desktop application",
            website="https://codeium.com/windsurf"
        ),
        "custom": Agent(
            id="custom",
            name="Custom Agent",
            description="Add your own AI tool or assistant",
            primary_use="Specialized or proprietary AI tools",
            access_method="As configured by your team",
            website=None
        )
    }
    
    @classmethod
    def get_agent(cls, agent_id: str) -> Optional[Agent]:
        """
        Get an agent by ID.
        
        Args:
            agent_id: The agent identifier
            
        Returns:
            Agent object or None if not found
        """
        return cls.AGENTS.get(agent_id.lower())
    
    @classmethod
    def get_all_agents(cls) -> List[Agent]:
        """
        Get all available agents.
        
        Returns:
            List of all Agent objects
        """
        return list(cls.AGENTS.values())
    
    @classmethod
    def get_agent_ids(cls) -> List[str]:
        """
        Get all agent IDs.
        
        Returns:
            List of agent IDs
        """
        return list(cls.AGENTS.keys())
    
    @classmethod
    def validate_agent_ids(cls, agent_ids: List[str]) -> tuple[List[str], List[str]]:
        """
        Validate a list of agent IDs.
        
        Args:
            agent_ids: List of agent IDs to validate
            
        Returns:
            Tuple of (valid_ids, invalid_ids)
        """
        valid = []
        invalid = []
        
        for agent_id in agent_ids:
            agent_id = agent_id.lower().strip()
            if agent_id in cls.AGENTS:
                valid.append(agent_id)
            else:
                invalid.append(agent_id)
        
        return valid, invalid
    
    @classmethod
    def parse_agent_string(cls, agent_string: str) -> List[str]:
        """
        Parse a comma-separated string of agent IDs.
        
        Args:
            agent_string: Comma-separated agent IDs (e.g., "claude,copilot,chatgpt")
            
        Returns:
            List of parsed agent IDs
        """
        if not agent_string:
            return []
        
        # Split by comma and clean up whitespace
        agents = [a.strip().lower() for a in agent_string.split(",") if a.strip()]
        return agents
    
    @classmethod
    def get_agent_choices_text(cls) -> str:
        """
        Get formatted text listing all available agents for prompts.
        
        Returns:
            Formatted string with agent choices
        """
        lines = ["Available agents:"]
        for i, agent in enumerate(cls.get_all_agents(), 1):
            lines.append(f"  {i}. {agent.name} - {agent.description}")
        return "\n".join(lines)
    
    @classmethod
    def get_agent_display_name(cls, agent_id: str) -> str:
        """
        Get the display name for an agent.
        
        Args:
            agent_id: The agent identifier
            
        Returns:
            Display name or the ID if not found
        """
        agent = cls.get_agent(agent_id)
        return agent.name if agent else agent_id
