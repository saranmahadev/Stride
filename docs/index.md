# Stride

**Agent-First Framework for Sprint-Powered, Spec-Driven Development**

Transform chaotic AI coding sessions into structured, trackable workflows.

[Get Started](#installation){ .md-button .md-button--primary }
[View on GitHub](https://github.com/saranmahadev/Stride){ .md-button }

---

## What is Stride?

Stride enables 20+ AI coding agents (Claude, Cursor, Windsurf, etc.) to autonomously plan, implement, and document software features while you monitor progress from the terminal.

### The Problem

AI coding has three major issues:

- **Context Loss** - AI forgets everything after a few chat turns
- **No Structure** - No methodology for AI-driven development
- **Can't Track** - Difficult to see what the AI actually implemented

### The Solution

Stride provides:

- **Sprint-Based Workflow** - Persistent context in markdown files
- **Slash Commands** - Clear workflows for 20+ AI agents
- **CLI Monitoring** - Real-time visibility from your terminal

---

## Installation

```bash
# Install from PyPI
pip install stridekit

# Verify installation
stride --version
```

---

## Quick Start

### 1. Initialize Your Project

```bash
stride init
```

Select your AI agents interactively (Cursor, Claude, Windsurf, etc.)

### 2. Start Your First Sprint

In your AI agent:

```
/stride:init
```

The agent will:

1. Create `project.md` with your project context
2. Start your first sprint with `proposal.md`
3. Guide you through planning and implementation

### 3. Monitor Progress

```bash
stride list      # View all sprints
stride status    # Check current state
stride show SPRINT-XXXXX  # Detailed sprint view
```

---

## Supported AI Agents

**20 AI Agents Across 5 Categories:**

| Category | Agents |
|----------|---------|
| **AI Editors** | Cursor, Windsurf |
| **Agents** | Cline, RooCode, Factory, OpenCode, KiloCode, Antigravity |
| **Assistants** | GitHub Copilot, Amazon Q, Auggie, iFlow, CodeBuddy, Costrict |
| **CLI Tools** | Gemini CLI, Claude Code, Qoder, Qwen, Codex |
| **Specialized** | Crush |

---

## Key Features

### Multi-Agent Support
- 20 AI agents supported
- 9 automatic template formats
- Unified methodology

### Sprint Management
- Lifecycle: Proposed → Active → Completed
- Real-time progress bars
- Task breakdown with strides

### Documentation System
- 6 sprint documents per sprint
- Version control friendly
- Human and AI readable

### Analytics
- Sprint metrics and insights
- Process compliance scoring
- Export to JSON/CSV

---

## Use Cases

!!! tip "For Indie Hackers"
    Ship features without losing context across chat sessions

!!! tip "For Startup CTOs"
    Align multiple AI tools with unified methodology

!!! tip "For Enterprise Developers"
    Trust AI with validation pipelines and audit trails

!!! tip "For AI-First Developers"
    Track exactly what agents implemented

---

## Requirements

- **Python**: 3.8+
- **OS**: Windows, macOS, Linux

---

## Learn More

- [CLI Commands](cli-commands.md) - Learn all CLI commands for monitoring
- [Agent Commands](agent-commands.md) - Understand agent slash commands
- [Sprint Lifecycle](sprint-lifecycle.md) - Master the sprint workflow
- [Philosophy](philosophy.md) - Understand Stride's principles

---

## Links

- [GitHub Repository](https://github.com/saranmahadev/Stride)
- [PyPI Package](https://pypi.org/project/stridekit/)
- [Report Issues](https://github.com/saranmahadev/Stride/issues)
