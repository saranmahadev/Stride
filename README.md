<div align="center">

![Stride Banner](https://raw.githubusercontent.com/saranmahadev/Stride/main/assets/images/banner.png)

# Stride

**Agent-First Framework for Sprint-Powered, Spec-Driven Development**

[![PyPI version](https://img.shields.io/badge/pypi-v1.0.1-blue.svg)](https://pypi.org/project/stridekit/)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[Website](https://stride.saranmahadev.in) • [Documentation](https://stride.saranmahadev.in) • [GitHub](https://github.com/saranmahadev/Stride)

</div>

---

## 🎯 What is Stride?

**Stride** transforms chaotic AI coding sessions into structured, trackable, and reproducible workflows. It enables 20+ AI coding agents (Claude, Cursor, Windsurf, etc.) to autonomously plan, implement, and document software features while you monitor progress from the terminal.

### The Problem

- 🔴 **Context Loss**: AI forgets everything after 3-5 chat turns
- 🔴 **No Structure**: No methodology for AI-driven development
- 🔴 **Can't Track**: What did the AI actually implement?
- 🔴 **Agent Chaos**: Multiple agents produce inconsistent outputs
- 🔴 **No Learning**: Retrospectives and learnings never captured

### Stride's Solution

- ✅ **Sprint-Based Structure** → Persistent context in markdown files
- ✅ **Slash Commands** → Clear workflows for 20+ AI agents
- ✅ **CLI Monitoring** → Real-time visibility from your terminal
- ✅ **Unified Methodology** → All agents follow the same process
- ✅ **Auto-Retrospectives** → Learnings captured automatically

---

## 🚀 Quick Start

### Installation

```bash
# Using pip
pip install stridekit

# Using uv (faster)
uv pip install stridekit

# Verify installation
stride --version
```

### Initialize Your Project

```bash
# 1. Initialize Stride in your project
stride init

# 2. Select your AI agents interactively
#    ✓ Cursor
#    ✓ Claude Code
#    ✓ Windsurf
#    ... and 17 more!

# 3. Stride installs slash commands for each agent
```

### Start Your First Sprint

In your AI agent (e.g., Cursor, Claude):
```
/stride:init
```

The agent will:
1. Create `project.md` with your project context
2. Start your first sprint with `proposal.md`
3. Guide you through planning and implementation

### Monitor Progress

```bash
stride list      # View all sprints
stride status    # Check current state
stride show SPRINT-XXXXX  # Detailed sprint view
stride metrics   # Analytics and insights
stride docs      # Serve documentation (MkDocs)
```

---

## 🤝 Team Collaboration (v1.5)

**Stride v1.5** brings Git-based team collaboration with zero infrastructure required. Small teams (2-10 developers) can now collaborate entirely through Git—no external tools, servers, or databases needed.

### Quick Team Setup

```bash
# 1. Initialize team configuration
stride team init

# 2. Add team members with roles
stride team add "Alice" alice@example.com --roles lead,reviewer
stride team add "Bob" bob@example.com --roles developer

# 3. Assign sprints with AI recommendations
stride assign sprint-feature-x
# → Shows AI-powered recommendations based on workload and expertise

# 4. Approve completed work
stride approve sprint-feature-x --by alice@example.com
stride approve status sprint-feature-x
# → Shows approval progress (1/2 required)
```

**Key Features:**
- 🏢 **Team Management** - Configure members, roles, and approval policies
- 🎯 **Smart Assignment** - AI-powered recommendations based on workload and skills
- ✅ **Approval Workflow** - N-reviewer policies with role-based permissions
- 💬 **Sprint Comments** - Threaded discussions with file/line anchoring
- ⚖️ **Workload Balancing** - Complexity scoring and distribution analysis
- 📊 **Team Metrics** - Workload visualization and balance scoring

All team data lives in `.stride/` directory, fully Git-versioned and portable. Works entirely offline—no cloud dependencies.

👉 [Read the complete Team Workflow Guide](https://stride.saranmahadev.in/team-workflow)

---

## ✨ Features

### 🤖 Multi-Agent Support (20 AI Agents)

| Category | Agents |
|----------|---------|
| **AI Editors** | Cursor, Windsurf |
| **Agents** | Cline, RooCode, Factory, OpenCode, KiloCode, Antigravity |
| **Assistants** | GitHub Copilot, Amazon Q, Auggie, iFlow, CodeBuddy, Costrict |
| **CLI Tools** | Gemini CLI, Claude Code, Qoder, Qwen, Codex |
| **Specialized** | Crush |

**9 Template Formats**: Automatically converts commands to each agent's format

### 🤝 Team Collaboration (Git-Based)

- **Zero Infrastructure**: Collaborate entirely through Git—no servers required
- **Team Management**: Members, roles, and approval policies
- **Smart Assignment**: AI-powered workload balancing
- **Approval Workflows**: N-reviewer policies with permissions
- **Sprint Comments**: Threaded discussions with code anchoring
- **Fully Offline**: All data in `.stride/` directory, Git-versioned

### 📊 Sprint Management

- **Lifecycle Tracking**: Proposed → Active → Completed
- **Progress Bars**: Real-time visual feedback
- **Task Breakdown**: Organize into strides (milestones) with subtasks
- **File-Based State**: Sprint status determined by which files exist

### 📝 Documentation System

Every sprint contains:
- `proposal.md` → What and why
- `plan.md` → How (strides, tasks, approach)
- `design.md` → Architecture and APIs
- `implementation.md` → Real-time development log
- `retrospective.md` → What worked, what didn't

**Benefits:**
- Version control tracks everything
- Human and AI readable
- No databases required
- Easy to audit and backup

### 📈 Analytics & Insights

```bash
stride metrics
```

- Sprint duration and completion rates
- Task distribution analysis
- Process compliance scoring
- Quality indicators
- Export to JSON/CSV

### 📚 Documentation Generation

```bash
/stride:docs     # Generate docs from completed sprints (in agent)
stride docs      # Serve documentation with MkDocs
```

- Automatically generates documentation from completed sprints
- Creates MkDocs-compatible site structure
- Extracts features, descriptions, and implementation details
- Serves interactive documentation at http://127.0.0.1:8000
- No sprint process details - only final product documentation

### ✅ Quality Gates & Validation

```bash
/stride:validate # Run comprehensive quality checks (in agent)
stride validate  # Validate sprint document structure (CLI)
```

- **Pre-completion quality gates** - Validates before `/stride:complete`
- **Auto-detection** - Detects project type and available tools
- **Comprehensive checks**:
  - Type checking (TypeScript, mypy, etc.)
  - Linting (ESLint, Pylint, Clippy, etc.)
  - Unit and integration tests
  - Security scanning for secrets and vulnerabilities
- **Smart status system**:
  - ✅ PASS - All checks passed
  - ❌ FAIL - Critical issues blocking completion
  - 🔜 UPCOMING - Will be fixed in future strides
- **Actionable reports** - Clear recommendations for fixing issues
- **Prevents broken completions** - Blocks sprint completion until critical issues resolved

### 🎨 Beautiful Terminal UI

- Color-coded status indicators
- ASCII progress bars
- Rich table displays
- Interactive prompts
- Spinners and animations

---

## 📖 How It Works

### 1. The Sprint Philosophy

Every feature, bug fix, or change is a **sprint**:

```
.stride/
  sprints/
    SPRINT-A3F2E/
      proposal.md          # ← What and why
      plan.md              # ← How (with strides)
      design.md            # ← Architecture
      implementation.md    # ← Development log
      retrospective.md     # ← Learnings
```

### 2. Agent Commands

When you run `stride init`, slash commands are installed:

| Command | Purpose |
|---------|---------|
| `/stride:init` | Create project spec and first sprint |
| `/stride:plan` | Define goals and break down tasks |
| `/stride:implement` | Build with implementation tracking |
| `/stride:status` | Check progress |
| `/stride:review` | Validate work |
| `/stride:validate` | Quality gates before completion |
| `/stride:complete` | Archive and retrospective |
| `/stride:docs` | Generate project documentation |
| `/stride:present` | Generate presentations |
| `/stride:derive` | Create sprint from existing |
| `/stride:lite` | Lightweight changes (< 50 lines) |
| `/stride:feedback` | Collect feedback |

### 3. CLI Monitoring

Monitor everything from your terminal:

```bash
$ stride list

┌─────────────┬──────────────────────────┬──────────┬─────────────┐
│ Sprint ID   │ Title                    │ Status   │ Created     │
├─────────────┼──────────────────────────┼──────────┼─────────────┤
│ SPRINT-A3F2E│ Add User Authentication  │ ACTIVE   │ 2 hours ago │
│ SPRINT-B7C9D│ Payment Integration      │ PROPOSED │ 1 day ago   │
└─────────────┴──────────────────────────┴──────────┴─────────────┘
```

---

## 🎯 Use Cases

### For Indie Hackers
Ship features without losing context across chat sessions. Every sprint is documented and tracked.

### For Startup CTOs
Align multiple AI tools (Cursor + Claude + Windsurf) with unified methodology and shared specs.

### For Enterprise Developers
Trust AI in legacy repos with validation pipelines, process compliance, and full audit trails.

### For AI-First Developers
Track exactly what agents implemented across sprints with full retrospective analysis.

---

## 📚 Documentation

- **[Website](https://stride.saranmahadev.in)** - Official documentation
- **[FEATURES.md](FEATURES.md)** - Complete feature list
- **[CHANGELOG.md](CHANGELOG.md)** - Version history
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
- **[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)** - Community guidelines

---

## 🛠️ Development

### Setup

```bash
# Clone repository
git clone https://github.com/saranmahadev/Stride.git
cd Stride

# Install in development mode
pip install -e ".[dev]"
```

### Code Quality

```bash
# Format code (Black, line length: 100)
black stride/

# Sort imports
isort stride/

# Type checking
mypy stride/

# Run tests
pytest

# With coverage
pytest --cov=stride --cov-report=html
```

### Project Structure

```
stride/
├── cli.py              # Typer CLI app
├── models.py           # Pydantic models
├── constants.py        # Constants and enums
├── utils.py            # Utility functions
├── commands/           # CLI commands (7)
│   ├── init.py
│   ├── list.py
│   ├── status.py
│   ├── show.py
│   ├── validate.py
│   ├── metrics.py
│   └── docs.py
├── core/               # Business logic
│   ├── sprint_manager.py
│   ├── markdown_parser.py
│   ├── agent_registry.py
│   ├── template_converter.py
│   ├── documentation_generator.py
│   └── analytics.py
└── templates/          # Templates
    ├── sprint_files/
    ├── agent_commands/
    └── agents_docs/
```

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Quick Contribution Steps

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting
5. Commit (`git commit -m 'Add amazing feature'`)
6. Push (`git push origin feature/amazing-feature`)
7. Open a Pull Request

---

## 📋 Requirements

- **Python**: 3.11+
- **OS**: Windows, macOS, Linux

### Dependencies

- `typer[all]` - CLI framework
- `rich` - Terminal formatting
- `pydantic` - Data validation
- `pyyaml` - YAML parsing
- `questionary` - Interactive prompts
- `pyfiglet` - ASCII art

---

## 🎓 Philosophy

Stride is built on three core principles:

1. **Agent-First Design** - AI agents do the work, humans provide direction
2. **Sprint-Based Methodology** - Structured workflow with clear phases
3. **Spec-Driven Development** - Everything documented in markdown

This creates **persistent context**, **cross-agent consistency**, and a **complete audit trail**.

---

## 📊 Stats

- **20 AI Agents** supported
- **9 Template Formats** for agent compatibility
- **7 CLI Commands** for monitoring
- **12 Agent Commands** for workflow
- **6 Sprint Documents** for each sprint

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🔗 Links

- **Website**: [stride.saranmahadev.in](https://stride.saranmahadev.in)
- **GitHub**: [github.com/saranmahadev/Stride](https://github.com/saranmahadev/Stride)
- **PyPI**: [pypi.org/project/stridekit](https://pypi.org/project/stridekit/)
- **Issues**: [github.com/saranmahadev/Stride/issues](https://github.com/saranmahadev/Stride/issues)

---

## 💖 Acknowledgments

Built with:
- [Typer](https://typer.tiangolo.com/) - CLI framework
- [Rich](https://rich.readthedocs.io/) - Terminal UI
- [Pydantic](https://docs.pydantic.dev/) - Data validation
- [PyYAML](https://pyyaml.org/) - YAML parsing
- [Questionary](https://questionary.readthedocs.io/) - Interactive prompts
- [Pyfiglet](https://github.com/pwaller/pyfiglet) - ASCII art

---

<div align="center">

**Made with ❤️ by [Saran Mahadev](https://stride.saranmahadev.in)**

⭐ Star us on [GitHub](https://github.com/saranmahadev/Stride) if you find Stride useful!

</div>
