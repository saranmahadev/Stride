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
- **DocumentationGenerator** ([stride/core/documentation_generator.py](stride/core/documentation_generator.py)) - Generates project documentation from completed sprints, creates MkDocs configuration
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
stride docs          # Start MkDocs server (port 8000 by default)
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

Docs dependencies (optional):
- **mkdocs** - Documentation site generator
- **mkdocs-material** - Material theme for MkDocs

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
│   ├── metrics.py           # Sprint analytics
│   └── docs.py              # Serve documentation
├── core/                     # Business logic
│   ├── sprint_manager.py    # Sprint CRUD operations
│   ├── markdown_parser.py   # Parse markdown files
│   ├── agent_registry.py    # Agent configurations
│   ├── template_converter.py # Convert templates
│   ├── documentation_generator.py # Generate docs
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

## Documentation System

Stride includes a documentation generation system that creates project documentation from completed sprints.

### Components

1. **`/stride:docs` Agent Command** ([stride/templates/agent_commands/docs.md](stride/templates/agent_commands/docs.md))
   - Analyzes all completed sprints (those with `retrospective.md`)
   - Extracts feature information, descriptions, and implementation details
   - Generates `docs/` folder with MkDocs-compatible documentation
   - Creates: `index.md`, `features.md`, `getting-started.md`, `mkdocs.yml`
   - Focuses on final product documentation, NOT sprint process

2. **`stride docs` CLI Command** ([stride/commands/docs.py](stride/commands/docs.py))
   - Starts MkDocs development server
   - Checks for `docs/mkdocs.yml` and creates basic config if missing
   - Serves documentation at `http://127.0.0.1:8000` (configurable port)
   - Requires MkDocs to be installed (`pip install mkdocs mkdocs-material`)

3. **DocumentationGenerator** ([stride/core/documentation_generator.py](stride/core/documentation_generator.py))
   - Core logic for documentation generation
   - Methods: `validate_project()`, `get_completed_sprints()`, `extract_features_from_sprints()`
   - Generates markdown files and MkDocs configuration
   - Creates basic structure that users can extend

### Workflow

```bash
# In AI agent (e.g., Claude, Cursor)
/stride:docs    # Generate documentation from completed sprints

# In terminal
stride docs     # Start MkDocs server to view documentation
```

### Documentation Structure

```
docs/
├── mkdocs.yml           # MkDocs configuration (Material theme)
├── index.md             # Project overview and feature list
├── features.md          # Detailed feature documentation
└── getting-started.md   # Installation and setup guide
```

### Key Principles

- **Source**: Only completed sprints (with `retrospective.md`)
- **Focus**: Final product features, not development process
- **Exclusions**: No sprint IDs, strides, implementation logs, or process details
- **Format**: Clean, user-facing documentation suitable for end users or API consumers
- **Customization**: Users can extend the generated docs with additional pages

## Quality Gates & Validation System

Stride includes both document validation (CLI) and comprehensive quality gates (agent command).

### Components

1. **`/stride:validate` Agent Command** ([stride/templates/agent_commands/validate.md](stride/templates/agent_commands/validate.md))
   - Runs comprehensive quality checks before sprint completion
   - Auto-detects project type and available validation tools
   - Executes: type checking, linting, tests, security scans
   - Generates structured validation report with Pass/Fail/Upcoming status
   - Prevents sprint completion if critical issues exist
   - Maps failures to sprint strides (upcoming fixes)

2. **`stride validate` CLI Command** ([stride/commands/validate.py](stride/commands/validate.py))
   - Validates sprint document structure against templates
   - Checks required sections, checkboxes, and content completeness
   - Ensures cross-file consistency
   - Detects template placeholders that need filling

3. **Validator** ([stride/core/validator.py](stride/core/validator.py))
   - Core logic for document structure validation
   - Template compliance checking
   - Section presence validation
   - Content completeness checks

### Quality Gate Categories

The `/stride:validate` agent command checks:

1. **Type Checking**: TypeScript (tsc), mypy, Flow, etc.
2. **Linting**: ESLint, Pylint, Flake8, Clippy, golangci-lint, etc.
3. **Tests**: Jest, pytest, JUnit, Cargo test, Go test, etc.
4. **Security**: Secret detection, dependency auditing
5. **Formatting**: Prettier, Black, rustfmt (warnings only)

### Validation Status Levels

- **✅ PASS**: All checks passed, ready for completion
- **❌ FAIL**: Critical issues blocking sprint completion
- **🔜 UPCOMING**: Will be fixed in future strides (documented in plan)
- **⏭️ SKIP**: Tool not configured or not applicable

### Workflow

```bash
# In AI agent (before completing sprint)
/stride:validate    # Run comprehensive quality gates

# In terminal (validate document structure)
stride validate SPRINT-AAAAA    # Validate specific sprint
stride validate --all           # Validate all sprints
```

### Key Principles

- **Pre-completion**: Always run `/stride:validate` before `/stride:complete`
- **Auto-detection**: Automatically detects project type and tools
- **Actionable**: Provides specific recommendations for fixing issues
- **Blocking**: Critical failures prevent sprint completion
- **Smart mapping**: Links failures to upcoming strides when applicable
- **Security-first**: Always checks for hardcoded secrets and vulnerabilities
