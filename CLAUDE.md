# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Stride** is an Agent-First Framework for Sprint-Powered, Spec-Driven Development. It enables AI coding agents to autonomously plan, implement, and document software features through a structured sprint-based workflow.

### Core Architecture

Stride follows a three-layer architecture:

1. **CLI Layer** ([stride/cli.py](stride/cli.py)) - Typer-based command registration and entry point
2. **Commands Layer** ([stride/commands/](stride/commands/)) - Individual command implementations (one per file)
3. **Core Layer** ([stride/core/](stride/core/)) - Business logic and managers

### Key Components

- **SprintManager** ([stride/core/sprint_manager.py](stride/core/sprint_manager.py)) - CRUD operations for sprints, status determination, progress calculation
- **MarkdownParser** ([stride/core/markdown_parser.py](stride/core/markdown_parser.py)) - Parses sprint files (checkboxes, strides, implementation logs)
- **AgentRegistry** ([stride/core/agent_registry.py](stride/core/agent_registry.py)) - Registry of 20 supported AI agents with their configurations
- **TemplateConverter** ([stride/core/template_converter.py](stride/core/template_converter.py)) - Converts Stride templates to 9 different agent-specific formats
- **Models** ([stride/models.py](stride/models.py)) - Pydantic models for Sprint, SprintProgress, StrideTask, CheckboxItem

### Sprint Lifecycle

Sprints exist in `.stride/sprints/SPRINT-{ID}/` and follow this state machine:

1. **PROPOSED** → `proposal.md` exists
2. **ACTIVE** → `implementation.md` exists
3. **COMPLETED** → `retrospective.md` exists

Status is determined by which files exist, not by explicit state markers.

## Development Commands

### Running the CLI

```bash
# Install in development mode
pip install -e .

# Run commands
stride --help
stride init
stride list
stride status
stride show SPRINT-AAAAA
stride validate
stride metrics
```

### Testing

```bash
# Run all tests with coverage
pytest

# Run specific test file
pytest tests/test_sprint_manager.py

# Run with verbose output
pytest -v

# Generate coverage report
pytest --cov=stride --cov-report=html
```

### Code Quality

```bash
# Format code with Black (line length: 100)
black stride/

# Sort imports
isort stride/

# Type checking
mypy stride/
```

### Building and Installing

```bash
# Build distribution
pip install build
python -m build

# Install from source
pip install .

# Uninstall
pip uninstall Stride
```

## File Organization

- **One command per file** in `stride/commands/` (e.g., `list.py`, `show.py`)
- **Business logic** in `stride/core/` (managers, parsers, converters)
- **Data models** in `stride/models.py` (Pydantic models)
- **Constants** in `stride/constants.py` (enums, paths, colors)
- **Templates** in `stride/templates/`:
  - `sprint_files/` - Sprint markdown templates (proposal, plan, etc.)
  - `agent_commands/` - Base agent command templates
  - `agents_docs/` - Agent documentation templates

## Agent Template System

Stride supports 20 AI agents across 9 format types. When adding new agent commands:

1. Create base template in `stride/templates/agent_commands/{command}.md` with YAML frontmatter
2. Mark conversion content between `<!-- STRIDE:START -->` and `<!-- STRIDE:END -->`
3. Add agent configuration to `AgentRegistry.AGENTS` if new agent
4. Converter will automatically generate agent-specific formats

Format types: `yaml-rich-metadata`, `yaml-name-id`, `yaml-arguments`, `yaml-xml-tags`, `yaml-auto-exec`, `yaml-github-copilot`, `toml`, `markdown-heading`, `no-frontmatter`

## Command Implementation Pattern

All commands follow this pattern:

```python
# stride/commands/example.py
import typer
from rich.console import Console
from ..core.sprint_manager import SprintManager

console = Console()

def example_command(
    arg: str,
    option: bool = typer.Option(False, "--option", "-o", help="Description")
):
    """
    Brief description of what this command does.

    Args:
        arg: Description of argument
        option: Description of option
    """
    # Use SprintManager for sprint operations
    manager = SprintManager()

    # Use Rich console for output
    console.print("[green]Success![/green]")
```

Then register in [stride/cli.py](stride/cli.py):

```python
from stride.commands import example
app.command(name="example")(example.example_command)
```

## Important Patterns

### Sprint Status Determination

Status is inferred from file existence (see `SprintManager._determine_status`):
- PROPOSED: Only `proposal.md` or `plan.md` exists
- ACTIVE: `implementation.md` exists
- COMPLETED: `retrospective.md` exists

### Progress Calculation

Progress is calculated by parsing markdown checkboxes in:
- **Strides** (in `plan.md`) - Task-level tracking
- **Acceptance Criteria** (in `proposal.md`) - High-level goals

Parsing logic in `MarkdownParser.parse_checkboxes()` and `MarkdownParser.parse_strides()`

### Rich Console Output

All commands use Rich library for formatted terminal output:
- Use `console.print()` for colored output
- Use `Table` for tabular data
- Use `Panel` for boxed content
- Use `Progress` for progress bars
- Color constants in `stride/constants.py`

## Dependencies

Core dependencies (see [pyproject.toml](pyproject.toml)):
- **typer[all]** - CLI framework
- **rich** - Terminal formatting
- **pyyaml** - YAML parsing
- **pydantic** - Data validation
- **pyfiglet** - ASCII art
- **questionary** - Interactive prompts

Dev dependencies:
- **pytest** + **pytest-cov** - Testing
- **black** - Code formatting (line length: 100)
- **isort** - Import sorting
- **mypy** - Type checking

## Project Structure

```
stride/
├── cli.py                    # Main Typer app
├── models.py                 # Pydantic models
├── constants.py              # Constants and enums
├── config.py                 # Configuration
├── utils.py                  # Utility functions
├── commands/                 # CLI commands (one per file)
│   ├── init.py              # Initialize Stride project
│   ├── list.py              # List all sprints
│   ├── status.py            # Show sprint status
│   ├── show.py              # Display sprint details
│   ├── validate.py          # Validate project structure
│   └── metrics.py           # Sprint analytics
├── core/                     # Business logic
│   ├── sprint_manager.py    # Sprint CRUD operations
│   ├── markdown_parser.py   # Parse markdown files
│   ├── agent_registry.py    # Agent configurations
│   ├── template_converter.py # Convert templates
│   ├── file_manager.py      # File operations
│   ├── validator.py         # Validation logic
│   ├── analytics.py         # Analytics engine
│   └── sprint_parser.py     # Sprint parsing
└── templates/                # Template files
    ├── sprint_files/        # Sprint markdown templates
    ├── agent_commands/      # Agent command templates
    └── agents_docs/         # Agent documentation
```

## Common Tasks

### Adding a New CLI Command

1. Create `stride/commands/new_command.py` following the command pattern
2. Register in `stride/cli.py`: `app.command(name="new-command")(new_command.new_command)`
3. Add any new business logic to `stride/core/`
4. Add tests if applicable

### Adding a New Agent

1. Add configuration to `AgentRegistry.AGENTS` in [stride/core/agent_registry.py](stride/core/agent_registry.py)
2. Specify: name, key, directory, extension, format_type
3. Run `stride init` to test template generation

### Modifying Sprint Structure

1. Update templates in `stride/templates/sprint_files/`
2. Update parsing logic in `MarkdownParser` if structure changes
3. Update `SprintManager` if status/progress calculation changes
4. Update models in `stride/models.py` if data structure changes
