# Changelog

All notable changes to Stride will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2025-01-08

### Added

- **Documentation Website** - Complete MkDocs documentation site
  - Custom red, white, and black theme
  - 8 comprehensive documentation pages
  - Deployed at stride.saranmahadev.in
  - Automatic deployment via GitHub Actions

### Changed

- **README Badge** - Fixed PyPI version badge display
- **Package Metadata** - Added docs optional dependencies

### Documentation

- **Introduction** - Complete getting started guide
- **CLI Commands** - Detailed command reference with examples
- **Agent Commands** - In-depth agent workflow documentation
- **Sprint Lifecycle** - Complete lifecycle explanation
- **Philosophy** - Design principles and rationale
- **Features** - Comprehensive feature overview
- **License** - MIT License documentation
- **Code of Conduct** - Community guidelines

---

## [1.0.0] - 2024-12-08

### Added - Core Features

#### Multi-Agent Support
- Support for 20 AI coding agents across 5 categories
- 9 template format types for agent-specific conversion
- Auto-configuration with interactive selection
- Agent registry system for managing configurations

#### CLI Commands
- `stride init` - Initialize Stride project with agent selection
- `stride list` - List all sprints with status badges
- `stride status` - Show current project status
- `stride show` - Display detailed sprint information
- `stride validate` - Validate project structure and sprint files
- `stride metrics` - Sprint analytics and statistics with JSON/CSV export

#### Agent Commands (10 slash commands)
- `/stride:init` - Create project spec and start first sprint
- `/stride:derive` - Derive new sprints from existing ones
- `/stride:lite` - Quick command reference
- `/stride:status` - Check sprint progress
- `/stride:plan` - Define sprint goals and tasks
- `/stride:present` - Generate sprint presentations
- `/stride:implement` - Implementation tracking
- `/stride:feedback` - Collect feedback
- `/stride:review` - Validate work
- `/stride:complete` - Complete sprint with retrospective

#### Sprint Management
- Sprint lifecycle: Proposed → Active → Completed
- File-based state determination
- Unique sprint IDs (SPRINT-XXXXX format)
- Progress tracking with strides and tasks
- Acceptance criteria tracking
- Implementation log parsing

#### Documentation System
- 6 sprint document templates (proposal, plan, design, implementation, retrospective, project)
- Markdown-based with version control support
- Automatic parsing of checkboxes, strides, and logs
- Section extraction and title detection

#### Analytics Engine
- Sprint metrics calculation (duration, completion rates, task distribution)
- Process compliance scoring
- Quality indicators (retrospective depth, learnings count)
- Trend analysis across sprints
- Export to JSON and CSV formats

#### Terminal UI
- Rich library integration for beautiful output
- Color-coded status indicators
- Progress bars and spinners
- ASCII art branding
- Interactive prompts with questionary
- Table-based data display

### Added - Architecture

#### Core Components
- `SprintManager` - CRUD operations for sprints
- `MarkdownParser` - Parse markdown files (checkboxes, strides, logs)
- `AgentRegistry` - Configuration registry for 20 agents
- `TemplateConverter` - Convert templates to 9 format types
- `Validator` - Project and sprint validation logic
- `Analytics` - Sprint analytics engine
- `MetricsCalculator` - Metrics computation

#### Data Models (Pydantic)
- `Sprint` - Sprint entity model
- `SprintProgress` - Progress tracking
- `StrideTask` - Stride (milestone) with tasks
- `CheckboxItem` - Markdown checkbox items
- `ImplementationLogEntry` - Implementation log entries
- `SprintData` - Analytics data class

#### Utilities
- Sprint ID generation (UUID-based)
- Progress bar rendering
- Timestamp formatting (relative and absolute)
- Text truncation and formatting
- Status colorization
- Task list formatting

### Added - Documentation
- Comprehensive README.md with quick start guide
- FEATURES.md with complete v1.0 feature list
- CLAUDE.md for Claude Code development guidance
- AGENTS.md for agent workflow documentation
- CHANGELOG.md (this file)

### Changed
- Updated version from 0.1.0 to 1.0.0
- Changed development status from Alpha to Production/Stable
- Removed all TODO comments and replaced with proper documentation
- Cleaned up unused imports (BarColumn, Progress, TaskID from utils.py)

### Fixed
- Documented placeholder functions in config.py
- Documented placeholder functions in file_manager.py
- Documented placeholder functions in templates/__init__.py
- All modules now have clear documentation about their current usage

### Technical Details

#### Dependencies
- typer[all] >= 0.9.0 (CLI framework)
- rich >= 13.0.0 (Terminal UI)
- pyyaml >= 6.0.0 (YAML parsing)
- pydantic >= 2.0.0 (Data validation)
- pyfiglet >= 0.8.post1 (ASCII art)
- questionary >= 2.0.0 (Interactive prompts)

#### Dev Dependencies
- pytest >= 7.0.0
- pytest-cov >= 4.0.0
- black >= 23.0.0 (line length: 100)
- isort >= 5.12.0
- mypy >= 1.0.0

#### Python Support
- Python >= 3.8
- Tested on Python 3.8, 3.9, 3.10, 3.11, 3.12

### Project Structure
```
stride/
├── cli.py                    # Main Typer app
├── models.py                 # Pydantic data models
├── constants.py              # Constants, enums, colors
├── utils.py                  # Utility functions
├── config.py                 # Configuration (placeholder)
├── commands/                 # CLI command implementations
│   ├── init.py              # Project initialization
│   ├── list.py              # List sprints
│   ├── status.py            # Project status
│   ├── show.py              # Sprint details
│   ├── validate.py          # Validation
│   └── metrics.py           # Analytics
├── core/                     # Business logic
│   ├── sprint_manager.py    # Sprint CRUD
│   ├── markdown_parser.py   # Markdown parsing
│   ├── agent_registry.py    # Agent configurations
│   ├── template_converter.py # Template conversion
│   ├── validator.py         # Validation logic
│   ├── analytics.py         # Analytics engine
│   ├── metrics_calculator.py # Metrics computation
│   └── sprint_parser.py     # Sprint file parsing
└── templates/                # Template files
    ├── sprint_files/        # Sprint document templates
    ├── agent_commands/      # Agent slash command templates
    └── agents_docs/         # Agent documentation
```

### Known Limitations
- No advanced configuration management (config.yaml not implemented)
- No database backend (file-based storage only)
- No web UI (CLI only)
- No CI/CD integration templates
- No plugin system (built-in agents only)

### Migration Guide
This is the first stable release. No migration needed.

### Contributors
- Saran Mahadev - Initial development and v1.0 release

---

## [Unreleased]

### Planned for Future Releases
- Advanced configuration management (config.yaml)
- Database backend option
- Web UI dashboard
- CI/CD integration templates
- Plugin system for custom agents
- Multi-language support
- Team collaboration features

---

[1.0.0]: https://github.com/saranmahadev/Stride/releases/tag/v1.0.0
