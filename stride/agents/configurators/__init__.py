"""
AI Tool Configurators

This package contains configurator implementations for 20+ AI coding assistants.
Each configurator knows how to integrate Stride workflows with its specific tool.
"""

# High Priority Tools (5)
from .claude import ClaudeConfigurator
from .cursor import CursorConfigurator
from .windsurf import WindsurfConfigurator
from .copilot import CopilotConfigurator
from .cline import ClineConfigurator

# Medium Priority Tools (8)
from .auggie import AuggieConfigurator
from .roocode import RooCodeConfigurator
from .codebuddy import CodeBuddyConfigurator
from .costrict import CoStrictConfigurator
from .crush import CrushConfigurator
from .factory import FactoryConfigurator
from .gemini import GeminiConfigurator
from .opencode import OpenCodeConfigurator

# Low Priority Tools (6)
from .kilo import KiloConfigurator
from .qoder import QoderConfigurator
from .antigravity import AntigravityConfigurator
from .codex import CodexConfigurator
from .amazonq import AmazonQConfigurator
from .qwen import QwenConfigurator

# Universal Fallback (1)
from .universal import UniversalConfigurator

# Auto-register all configurators
from ..registry import ToolRegistry

# High Priority
ToolRegistry.register(ClaudeConfigurator())
ToolRegistry.register(CursorConfigurator())
ToolRegistry.register(WindsurfConfigurator())
ToolRegistry.register(CopilotConfigurator())
ToolRegistry.register(ClineConfigurator())

# Medium Priority
ToolRegistry.register(AuggieConfigurator())
ToolRegistry.register(RooCodeConfigurator())
ToolRegistry.register(CodeBuddyConfigurator())
ToolRegistry.register(CoStrictConfigurator())
ToolRegistry.register(CrushConfigurator())
ToolRegistry.register(FactoryConfigurator())
ToolRegistry.register(GeminiConfigurator())
ToolRegistry.register(OpenCodeConfigurator())

# Low Priority
ToolRegistry.register(KiloConfigurator())
ToolRegistry.register(QoderConfigurator())
ToolRegistry.register(AntigravityConfigurator())
ToolRegistry.register(CodexConfigurator())
ToolRegistry.register(AmazonQConfigurator())
ToolRegistry.register(QwenConfigurator())

# Universal
ToolRegistry.register(UniversalConfigurator())

__all__ = [
    # High Priority
    'ClaudeConfigurator',
    'CursorConfigurator',
    'WindsurfConfigurator',
    'CopilotConfigurator',
    'ClineConfigurator',
    # Medium Priority
    'AuggieConfigurator',
    'RooCodeConfigurator',
    'CodeBuddyConfigurator',
    'CoStrictConfigurator',
    'CrushConfigurator',
    'FactoryConfigurator',
    'GeminiConfigurator',
    'OpenCodeConfigurator',
    # Low Priority
    'KiloConfigurator',
    'QoderConfigurator',
    'AntigravityConfigurator',
    'CodexConfigurator',
    'AmazonQConfigurator',
    'QwenConfigurator',
    # Universal
    'UniversalConfigurator',
]
