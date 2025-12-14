# Changelog

All notable changes to Stride will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.5.0] - 2025-12-14

### Added

#### Team Collaboration Features (ROADMAP.md Phase 2)

Stride v1.5 introduces Git-based team collaboration for small teams (2-10 developers). Zero infrastructure required—all team data lives in `.stride/` directory, fully Git-versioned and portable.

#### Team Management Commands
- `stride team init` - Initialize team configuration with members and approval policies
- `stride team add <name> <email>` - Add team member with roles
- `stride team remove <email>` - Remove team member with safeguards
- `stride team edit <email>` - Update member name or roles
- `stride team list` - Display all members with roles and approval policy
- `stride team show <email>` - Show detailed member information

#### Sprint Assignment Commands
- `stride assign <sprint-id>` - Assign sprint with AI-powered recommendations
  - Interactive mode shows top 5 recommendations based on workload, roles, and history
  - AI scoring factors: workload (0-3+ sprints), roles (lead +15, developer +5), recent assignments (-10)
- `stride unassign <sprint-id>` - Remove sprint assignment
- `stride assign workload [email]` - View workload distribution with complexity scoring
  - Team-wide or individual member views
  - Visual progress bars and balance scoring
  - JSON export support via `--export` flag

#### Approval Workflow Commands
- `stride approve <sprint-id>` - Approve sprint with role-based permissions
- `stride approve revoke <sprint-id> <email>` - Revoke approval
- `stride approve status <sprint-id>` - Show approval progress with visual feedback
- `stride approve pending` - List sprints awaiting approval

#### Comment & Communication Commands
- `stride comment add <sprint-id> <content>` - Add comment with optional file/line anchoring
- `stride comment list <sprint-id>` - Display threaded comments with Rich Tree visualization
- `stride comment resolve <sprint-id> <comment-id>` - Mark comment as resolved
- `stride comment unresolve <sprint-id> <comment-id>` - Reopen resolved comment
- `stride comment stats <sprint-id>` - Show comment statistics

#### Core Modules
- `stride/core/team_file_manager.py` - Atomic file operations for team.yaml, metadata.yaml, comments.yaml
- `stride/core/assignment_manager.py` - Sprint assignment logic with AI recommendations
- `stride/core/approval_manager.py` - Role-based approval workflow management
- `stride/core/comment_manager.py` - Threaded comment system with resolution tracking
- `stride/core/workload_analyzer.py` - Complexity scoring and workload distribution analysis

#### Command Modules
- `stride/commands/team.py` - Team management CLI (7 commands)
- `stride/commands/assign.py` - Assignment and workload commands (3 commands)
- `stride/commands/approve.py` - Approval workflow commands (4 commands)
- `stride/commands/comment.py` - Comment system commands (6 commands)

#### Data Models (Pydantic v2.0+)
- `TeamConfig` - Team configuration with members, roles, approval policy
- `TeamMember` - Member profile with email, name, roles, joined date
- `SprintMetadata` - Sprint assignment, approvals, status, history
- `Comment` - Threaded comments with optional file/line anchoring
- `Approval` - Approval record with approver, timestamp, comment
- `ApprovalPolicy` - Policy configuration (N reviewers, role restrictions)
- `MetadataEvent` - History event tracking for assignments and approvals

#### Workload Balancing System
- **Complexity Scoring**: `(stride_count × 5) + task_count` normalized to 0-100 scale
- **Balance Score**: `100 - (std_dev as % of mean)`, higher = more balanced distribution
- Identifies overloaded members (>1.5× average load)
- Identifies underutilized members (<0.5× average load)
- Natural language recommendations for load balancing
- Visual workload distribution with Rich progress bars

### Changed

#### Enhanced Commands
- `stride list` - Added `--assignee <email>` filter to show sprints for specific member
- `stride list` - Added assignee column in both verbose and compact views
- `stride metrics` - Integrated team workload panel with balance scoring
  - Shows team size, total sprints, average load, load range, balance score
  - Gracefully skips if no team configuration (backward compatible)

### Notes

#### Backward Compatibility
- **Fully compatible** with v1.0 solo workflows - all team features are optional
- Projects without `team.yaml` work exactly like v1.0 (solo mode)
- All existing sprint files fully compatible
- All 10 agent commands work identically
- No breaking changes to CLI or file formats

#### Git-Based Collaboration Model
- **Zero Infrastructure**: No servers, databases, or cloud dependencies required
- **Fully Offline**: Complete team collaboration without internet connection
- **Privacy-First**: All data stays in repository, no external services
- **Portable**: Team data moves with repository (clone → collaborate)
- **Audit Trail**: Full history tracked in Git commits

#### Architecture
- Atomic file operations prevent corruption (tempfile + shutil.move pattern)
- YAML safe_load/safe_dump for security
- Rich terminal formatting for all team commands
- Comprehensive docstrings and type hints throughout

#### Performance
- All commands complete within 2-second threshold
- Workload calculations cached for large teams
- No database overhead (file-based state)

#### ROADMAP Alignment
- Completes Phase 2 (v1.5): Repo-Based Team Collaboration
- Foundation for Phase 3 (v1.6-v1.8): Cloud-Optional Hybrid Collaboration
- Scales gracefully: Solo → Team → Enterprise without rewrites

---

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
