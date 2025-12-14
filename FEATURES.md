# Stride v1.0 Features Summary

**Stride v1.0** is a production-ready Agent-First Framework for Sprint-Powered, Spec-Driven Development.

## Core Features

### 1. Sprint-Based Development Workflow

- **Sprint Lifecycle Management**: Structured workflow from Proposed → Active → Completed
- **File-Based State**: Sprint status determined by which files exist (proposal, implementation, retrospective)
- **Sprint Organization**: All sprints organized in `.stride/sprints/SPRINT-{ID}/` directories
- **Unique Sprint IDs**: Auto-generated 5-character uppercase hex identifiers (e.g., `SPRINT-A3F2E`)

### 2. Multi-Agent Support (20 AI Agents)

Stride supports 20 different AI coding agents across 5 categories:

#### AI Editors
- **Cursor** - AI-powered code editor
- **Windsurf** - Flow-based coding agent

#### Agents
- **Cline** - VS Code extension for autonomous coding
- **RooCode** - Kangaroo-themed coding assistant
- **Factory Droid** - Code factory automation agent
- **OpenCode** - Open-source coding agent
- **KiloCode** - Scalable code generation
- **Antigravity** - Zero-gravity coding experience

#### Assistants
- **GitHub Copilot** - GitHub's AI pair programmer
- **Amazon Q** - AWS's AI coding assistant
- **Auggie** - Augment's AI coding assistant
- **iFlow** - Flow-based AI coding assistant
- **CodeBuddy** - AI pair programming assistant
- **Costrict** - Constraint-based coding agent

#### CLI Tools
- **Gemini CLI** - Google's Gemini for command line
- **Claude Code** - Anthropic's Claude with code execution
- **Qoder** - Quality-focused code generator
- **Qwen** - Alibaba's Qwen coding model
- **Codex** - OpenAI Codex integration

#### Specialized
- **Crush** - High-performance code crusher

### 3. Template Conversion System

- **9 Format Types**: Automatically converts templates to agent-specific formats
  - `yaml-rich-metadata` (Claude, CodeBuddy, Crush, Qoder)
  - `yaml-name-id` (Cursor, iFlow)
  - `yaml-arguments` (Codex, Auggie, Factory)
  - `yaml-xml-tags` (Amazon Q, OpenCode)
  - `yaml-auto-exec` (Windsurf)
  - `yaml-github-copilot` (GitHub Copilot)
  - `toml` (Qwen, Gemini, Codex)
  - `markdown-heading` (Cline, RooCode)
  - `no-frontmatter` (KiloCode)

- **10 Agent Commands**: Automatically generated for each agent
  - `/stride:init` - Create project spec and start first sprint
  - `/stride:derive` - Create new sprints from existing ones
  - `/stride:lite` - Lightweight changes without sprint files
  - `/stride:status` - Check current sprint progress
  - `/stride:plan` - Define sprint goals and break down tasks
  - `/stride:present` - Generate sprint presentations
  - `/stride:implement` - Build features with implementation tracking
  - `/stride:feedback` - Collect and organize feedback
  - `/stride:review` - Validate work and gather feedback
  - `/stride:complete` - Archive sprint and document learnings

### 4. Rich CLI Commands

#### `stride init`
- Interactive agent selection with checkbox UI
- Automatic directory structure creation
- Agent-specific command installation
- Beautiful ASCII art banner
- Progress indicators and spinners

#### `stride list`
- Display all sprints with status badges
- Color-coded status indicators (Proposed/Active/Completed)
- Creation timestamps
- Sprint titles and IDs
- Summary statistics

#### `stride status`
- Overall project status
- Active sprints summary
- Progress bars and completion percentages
- Recent activity tracking

#### `stride show <SPRINT-ID>`
- Detailed sprint information
- Stride-level task breakdown
- Acceptance criteria tracking
- Implementation log viewing
- Progress visualization with Rich tables

---

## Team Collaboration (v1.5)

**Stride v1.5** introduces Git-based team collaboration for small teams (2-10 developers). All team data lives in `.stride/` directory, fully Git-versioned and portable. Zero infrastructure required—works entirely offline.

### Philosophy

Stride's team collaboration follows a **repo-first, zero-infrastructure** model:

- **No servers**: Collaborate entirely through Git push/pull
- **No databases**: All state in YAML files version-controlled by Git
- **No cloud dependency**: Fully offline-capable (cloud optional in v1.6+)
- **Privacy-first**: All data stays in your repository
- **Graceful scaling**: Solo → Team → Enterprise without rewrites

This enables small teams to adopt Stride without external project management tools, maintaining the same developer experience that made v1.0 successful for solo developers.

### 1. Team Management Commands

#### `stride team init`

Initialize team collaboration in your Stride project.

**Syntax:**
```bash
stride team init [--force]
```

**What it does:**
- Creates `.stride/team.yaml` with team configuration
- Collects team members interactively (press Enter to finish)
- Configures approval policy (N required reviewers)
- Defines role-based permissions

**Example:**
```bash
$ stride team init

Enter project name: MyApp
Add Team Members (Press Enter with empty name to finish)

Member name: Alice Johnson
Email: alice@example.com
Roles (comma-separated): lead,reviewer

✓ Added Alice Johnson

Member name: Bob Smith
Email: bob@example.com
Roles (comma-separated): developer

✓ Added Bob Smith

Member name: [Enter]

Approval Policy
Enable approval workflow? [y/n]: y
Required approvals: 2
Roles that can approve (comma-separated): lead,reviewer

✓ Team configuration created!
File: .stride/team.yaml
2 team members configured
Approval workflow: enabled
```

**Parameters:**
- `--force`: Overwrite existing team.yaml

**Exit Codes:**
- 0: Success
- 1: Error

---

#### `stride team add`

Add a new team member.

**Syntax:**
```bash
stride team add <name> <email> [--roles ROLES]
```

**Example:**
```bash
stride team add "Carol Lee" carol@example.com --roles developer,reviewer
```

**Parameters:**
- `name` (required): Member's full name
- `email` (required): Unique email address (used as identifier)
- `--roles`: Comma-separated roles (default: developer)

**Available Roles:**
- `lead`: Team lead with full permissions
- `developer`: Can be assigned and implement sprints
- `reviewer`: Can approve sprints
- `designer`: Design-focused role
- `qa`: Quality assurance role
- `docs`: Documentation specialist

---

#### `stride team list`

Display all team members with their roles and approval policy.

**Syntax:**
```bash
stride team list
```

**Example Output:**
```
┌───────────────────┬────────────────────┬────────────────┬─────────┬────────────┐
│ Name              │ Email              │ Roles          │ Active  │ Joined     │
├───────────────────┼────────────────────┼────────────────┼─────────┼────────────┤
│ Alice Johnson     │ alice@example.com  │ lead,reviewer  │ ✓       │ 2 days ago │
│ Bob Smith         │ bob@example.com    │ developer      │ ✓       │ 2 days ago │
│ Carol Lee         │ carol@example.com  │ dev,reviewer   │ ✓       │ 1 hour ago │
└───────────────────┴────────────────────┴────────────────┴─────────┴────────────┘

Approval Policy
Workflow Enabled: Yes
Required Approvals: 2
Roles Can Approve: lead, reviewer
```

---

#### `stride team show <email>`

Show detailed information for a specific team member.

**Syntax:**
```bash
stride team show <email>
```

**Example:**
```bash
$ stride team show alice@example.com

╭─────────────── Alice Johnson ───────────────╮
│                                              │
│ Email:   alice@example.com                   │
│ Roles:   lead, reviewer                      │
│ Active:  Yes                                 │
│ Joined:  2024-12-12 10:30:00                 │
│                                              │
╰──────────────────────────────────────────────╯
```

---

#### `stride team edit <email>`

Update team member information.

**Syntax:**
```bash
stride team edit <email> [--name NAME] [--roles ROLES]
```

**Example:**
```bash
stride team edit alice@example.com --roles lead,reviewer,developer
```

**Parameters:**
- `--name`: Update member name
- `--roles`: Update roles (comma-separated)

**Note:** Email address cannot be changed (used as unique identifier).

---

#### `stride team remove <email>`

Remove a team member.

**Syntax:**
```bash
stride team remove <email> [--force]
```

**Example:**
```bash
stride team remove carol@example.com
```

**Safeguards:**
- Prompts for confirmation unless `--force` used
- Blocks removal if member has active sprint assignments
- Preserves historical data (approvals, comments remain)

---

### 2. Sprint Assignment Commands

#### `stride assign <sprint-id>`

Assign a sprint to a team member with optional AI-powered recommendations.

**Syntax:**
```bash
stride assign <sprint-id> [--to EMAIL] [--by EMAIL]
```

**Interactive Mode (No --to flag):**
Shows AI-powered recommendations based on:
- Current workload (sprints per member)
- Member roles (lead +15 points, developer +5)
- Assignment history (recent assignments -10)

**Example:**
```bash
$ stride assign sprint-feature-x

AI-Powered Assignment Recommendations for sprint-feature-x

┌────┬────────────────────┬───────┬────────────────────────────────────┐
│ #  │ Member             │ Score │ Reason                             │
├────┼────────────────────┼───────┼────────────────────────────────────┤
│ 1  │ Bob Smith          │ 130   │ No current assignments (+30)       │
│ 2  │ Carol Lee          │ 115   │ Light workload (1 sprint)          │
│ 3  │ Alice Johnson      │ 95    │ Lead role (+15), moderate workload │
└────┴────────────────────┴───────┴────────────────────────────────────┘

Select assignee (1-3) or email: 1

✓ Assigned sprint-feature-x to Bob Smith
```

**Direct Mode (With --to flag):**
```bash
stride assign sprint-feature-x --to bob@example.com
```

**Parameters:**
- `sprint-id` (required): Sprint identifier
- `--to EMAIL`: Direct assignment to specific member
- `--by EMAIL`: Attribution (who made the assignment)

---

#### `stride unassign <sprint-id>`

Remove sprint assignment.

**Syntax:**
```bash
stride unassign <sprint-id> [--force]
```

**Example:**
```bash
stride unassign sprint-feature-x
```

---

#### `stride assign workload [email]`

View workload distribution across team or for specific member.

**Syntax:**
```bash
stride assign workload [email] [--export]
```

**Team-Wide View:**
```bash
$ stride assign workload

╭─────────────── Team Workload Distribution ───────────────╮
│                                                           │
│ Team Size: 3 members                                      │
│ Total Sprints: 5                                          │
│ Average Load: 1.67 sprints/member                         │
│ Balance Score: 85/100 (Well Balanced)                     │
│                                                           │
╰───────────────────────────────────────────────────────────╯

┌────────────────────┬────────┬─────────┬──────────┬──────────────┐
│ Member             │ Active │ Pending │ Weighted │ Load Bar     │
├────────────────────┼────────┼─────────┼──────────┼──────────────┤
│ Alice Johnson      │ 2      │ 1       │ 45       │ ████████░░░░ │
│ Bob Smith          │ 1      │ 0       │ 20       │ ████░░░░░░░░ │
│ Carol Lee          │ 1      │ 0       │ 18       │ ███░░░░░░░░░ │
└────────────────────┴────────┴─────────┴──────────┴──────────────┘

Recommendations:
→ Workload is well balanced across team
→ Alice has moderate load but within acceptable range
```

**Individual View:**
```bash
$ stride assign workload alice@example.com

╭─────────────── Alice Johnson's Workload ───────────────╮
│                                                         │
│ Active Sprints: 2                                       │
│ Pending: 1                                              │
│ Completed: 8                                            │
│ Complexity Score: 45/100                                │
│                                                         │
╰─────────────────────────────────────────────────────────╯
```

**JSON Export:**
```bash
stride assign workload --export > workload.json
```

**Workload Complexity Scoring:**

Sprint complexity = `(stride_count × 5) + task_count`

Normalized to 0-100 scale assuming max realistic complexity is 150 points.

**Balance Score:**

Balance score = `100 - (std_dev as % of mean)`

Higher score = more balanced distribution. Score > 70 is considered well balanced.

---

### 3. Approval Workflow Commands

#### `stride approve <sprint-id>`

Approve a completed sprint.

**Syntax:**
```bash
stride approve <sprint-id> [--by EMAIL] [--comment TEXT]
```

**Example:**
```bash
stride approve sprint-feature-x --by alice@example.com --comment "LGTM, great work!"
```

**Approval Workflow:**
1. Validates approver has permission (role-based)
2. Checks for duplicate approval (one approval per member)
3. Adds approval to sprint metadata
4. Logs event to history

**Parameters:**
- `sprint-id` (required): Sprint identifier
- `--by EMAIL`: Approver email (required unless git identity detected)
- `--comment TEXT`: Optional approval comment

**Exit Codes:**
- 0: Approval successful
- 1: Permission denied, duplicate approval, or sprint not found

---

#### `stride approve status <sprint-id>`

Show approval status with visual progress.

**Syntax:**
```bash
stride approve status <sprint-id>
```

**Example Output:**
```bash
$ stride approve status sprint-feature-x

╭─────────────── Approval Status: sprint-feature-x ───────────────╮
│                                                                  │
│ Workflow Enabled: Yes                                            │
│ Required Approvals: 2                                            │
│ Current Approvals: 1                                             │
│                                                                  │
│ Progress: [████████████░░░░░░░░░░░░] 50% (1/2)                   │
│                                                                  │
│ Can Complete: No (1 more approval needed)                        │
│                                                                  │
╰──────────────────────────────────────────────────────────────────╯

Approvals Received:
┌───────────────────┬─────────────────────┬──────────────────┐
│ Approver          │ Timestamp           │ Comment          │
├───────────────────┼─────────────────────┼──────────────────┤
│ Alice Johnson     │ 2024-12-14 10:30:00 │ LGTM             │
└───────────────────┴─────────────────────┴──────────────────┘
```

---

#### `stride approve pending [--by EMAIL]`

List all sprints pending approval.

**Syntax:**
```bash
stride approve pending [--by EMAIL]
```

**Example:**
```bash
$ stride approve pending

Sprints Pending Approval

┌──────────────────┬───────────────────────┬────────────┬──────────────┐
│ Sprint ID        │ Title                 │ Assignee   │ Approvals    │
├──────────────────┼───────────────────────┼────────────┼──────────────┤
│ sprint-feature-x │ Add User Profile      │ Bob Smith  │ 1/2          │
│ sprint-bugfix-y  │ Fix Login Issue       │ Carol Lee  │ 0/2          │
└──────────────────┴───────────────────────┴────────────┴──────────────┘
```

**Filtered View:**
```bash
stride approve pending --by alice@example.com
```
Shows only sprints awaiting approval from Alice.

---

#### `stride approve revoke <sprint-id> <email>`

Revoke a previously given approval.

**Syntax:**
```bash
stride approve revoke <sprint-id> <email>
```

**Example:**
```bash
stride approve revoke sprint-feature-x alice@example.com
```

---

### 4. Comment & Communication Commands

#### `stride comment add <sprint-id> <content>`

Add a comment to a sprint with optional file/line anchoring.

**Syntax:**
```bash
stride comment add <sprint-id> <content> [OPTIONS]
```

**Options:**
- `--by EMAIL`: Comment author
- `--file PATH`: Anchor to specific file
- `--line NUMBER`: Anchor to specific line
- `--reply-to ID`: Reply to existing comment (threading)

**Examples:**

General comment:
```bash
stride comment add sprint-feature-x "Great progress on the authentication!"
```

Code-anchored comment:
```bash
stride comment add sprint-feature-x "This function needs error handling" \
  --file src/auth.py --line 42 --by alice@example.com
```

Threaded reply:
```bash
stride comment add sprint-feature-x "Done! Added try/catch block" \
  --reply-to c1702573890123 --by bob@example.com
```

---

#### `stride comment list <sprint-id>`

Display all comments for a sprint with threading.

**Syntax:**
```bash
stride comment list <sprint-id> [OPTIONS]
```

**Options:**
- `--unresolved`: Show only unresolved comments
- `--file PATH`: Filter by file
- `--flat`: Flat table view (no threading)

**Threaded View (Default):**
```bash
$ stride comment list sprint-feature-x

Comments for sprint-feature-x

sprint-feature-x
├── c1702573890123 [○] Alice Johnson (src/auth.py:42)
│   "This function needs error handling"
│   └── c1702573891456 [✓] Bob Smith
│       "Done! Added try/catch block"
└── c1702573892789 [○] Carol Lee
    "Consider adding unit tests"
```

**Flat Table View:**
```bash
stride comment list sprint-feature-x --flat

┌─────────────────┬────────────────┬────────┬──────────────┬──────────────────────────┐
│ ID              │ Author         │ Status │ File:Line    │ Content                  │
├─────────────────┼────────────────┼────────┼──────────────┼──────────────────────────┤
│ c1702573890123  │ Alice Johnson  │ ✓      │ auth.py:42   │ This function needs...   │
│ c1702573891456  │ Bob Smith      │ ✓      │ auth.py:42   │ Done! Added try/catch... │
│ c1702573892789  │ Carol Lee      │ ○      │ -            │ Consider adding tests    │
└─────────────────┴────────────────┴────────┴──────────────┴──────────────────────────┘

Legend: ✓ = Resolved, ○ = Unresolved
```

---

#### `stride comment resolve <sprint-id> <comment-id>`

Mark a comment as resolved.

**Syntax:**
```bash
stride comment resolve <sprint-id> <comment-id> [--by EMAIL]
```

**Example:**
```bash
stride comment resolve sprint-feature-x c1702573890123 --by bob@example.com
```

---

#### `stride comment unresolve <sprint-id> <comment-id>`

Mark a resolved comment as unresolved (reopen).

**Syntax:**
```bash
stride comment unresolve <sprint-id> <comment-id>
```

---

#### `stride comment stats <sprint-id>`

Show comment statistics for a sprint.

**Syntax:**
```bash
stride comment stats <sprint-id>
```

**Example Output:**
```bash
$ stride comment stats sprint-feature-x

╭─────────────── Comment Statistics ───────────────╮
│                                                   │
│ Total Comments: 12                                │
│ Unresolved: 3                                     │
│ Resolved: 9                                       │
│                                                   │
│ Files with Comments:                              │
│ • src/auth.py (5 comments)                        │
│ • src/utils.py (3 comments)                       │
│ • tests/test_auth.py (4 comments)                 │
│                                                   │
╰───────────────────────────────────────────────────╯
```

---

### 5. Enhanced CLI Commands

#### `stride list --assignee <email>`

Filter sprints by assignee.

**Example:**
```bash
stride list --assignee bob@example.com
```

Shows only sprints assigned to Bob.

---

#### `stride metrics`

Includes team workload panel when team configured.

**Example Output:**
```bash
$ stride metrics

[...existing metrics...]

╭─────────────── Team Workload Metrics ───────────────╮
│                                                      │
│ Team Size: 3 members                                 │
│ Total Sprints: 5                                     │
│ Average Load: 1.67 sprints/member                    │
│ Load Range: 1-2 sprints                              │
│ Balance Score: 85/100                                │
│                                                      │
╰──────────────────────────────────────────────────────╯
```

---

### Git-Based Collaboration Model

**How it Works:**

1. **Team Setup**: Run `stride team init` to create `.stride/team.yaml`
2. **Git Commit**: Commit team.yaml to repository
3. **Team Sync**: Other members pull repository to see team config
4. **Sprint Assignment**: Assign sprints, metadata stored in `.stride/sprints/<ID>/.metadata.yaml`
5. **Approval Workflow**: Approvals written to metadata, tracked in Git history
6. **Comments**: Discussions in `.stride/sprints/<ID>/.comments.yaml`
7. **Version Control**: All team data version-controlled, full audit trail

**Benefits:**

- ✅ **No External Tools**: No Jira, Linear, or project management SaaS required
- ✅ **Fully Offline**: Works without internet connection
- ✅ **Git Audit Trail**: All changes tracked in Git history
- ✅ **Conflict Resolution**: Git handles concurrent changes
- ✅ **Portable**: Team data moves with repository
- ✅ **Privacy-First**: No data sent to external servers

**File Structure:**

```
.stride/
├── team.yaml                       # Team configuration
└── sprints/
    └── sprint-feature-x/
        ├── proposal.md
        ├── plan.md
        ├── design.md
        ├── implementation.md
        ├── .metadata.yaml         # Assignment & approvals
        └── .comments.yaml         # Sprint discussions
```

---

### Backward Compatibility

All team features are **optional**. Stride v1.5 fully supports solo workflows:

- No `team.yaml`? Solo mode works exactly like v1.0
- No team commands used? Existing CLI behavior unchanged
- Sprint files? Fully compatible with v1.0 structure
- Agent commands? All 10 agent commands work identically

Team collaboration is additive—zero breaking changes.

#### `stride validate`
- Project structure validation
- Sprint file existence checks
- Markdown format validation
- Configuration verification
- Detailed error reporting

#### `stride metrics`
- Sprint analytics and statistics
- Completion rates and trends
- Task distribution analysis
- Process compliance scoring
- Export to JSON/CSV formats

### 5. Advanced Markdown Parsing

- **Checkbox Parsing**: Extract and track `[ ]` and `[x]` checkboxes
- **Stride Parsing**: Parse hierarchical stride structures from plan.md
- **Section Extraction**: Extract specific markdown sections by heading
- **Title Extraction**: Automatic title detection from H1 headings
- **Implementation Logs**: Parse timestamped implementation entries
- **Progress Calculation**: Automatic completion percentage calculation

### 6. Sprint Document Templates

Six core sprint documents:

1. **proposal.md** - Problem statement, goals, acceptance criteria
2. **plan.md** - Strides (milestones), tasks, approach, risks
3. **design.md** - Architecture, diagrams, APIs, technical specs
4. **implementation.md** - Real-time development log, decisions, changes
5. **retrospective.md** - What worked, what didn't, lessons learned
6. **project.md** - Project overview and context (root level)

### 7. Progress Tracking System

- **Stride-Level Tracking**: Break down work into numbered strides (milestones)
- **Task-Level Tracking**: Checkbox-based task completion within each stride
- **Acceptance Criteria**: High-level goal tracking separate from implementation tasks
- **Completion Definitions**: Clear "done" criteria for each stride
- **Progress Visualization**: ASCII progress bars and percentage displays

### 8. Analytics Engine

- **Sprint Metrics**: Duration, completion rates, task statistics
- **Process Compliance**: Track which documents exist (planning, implementation, retrospective)
- **Quality Indicators**: Retrospective depth, learnings captured
- **Trend Analysis**: Compare sprints over time
- **Export Capabilities**: JSON and CSV export for external analysis

### 9. Beautiful Terminal UI

Built with Rich library:
- **Color-Coded Output**: Status badges, progress bars, syntax highlighting
- **Tables**: Structured data display with borders and alignment
- **Panels**: Boxed content with titles and borders
- **Progress Bars**: Visual feedback for long-running operations
- **Spinners**: Activity indicators during processing
- **ASCII Art**: Brand identity with pyfiglet

### 10. Developer Experience

- **Interactive Prompts**: Questionary-powered checkbox and confirmation dialogs
- **Helpful Error Messages**: Clear, actionable error descriptions
- **Verbose Mode**: Optional detailed output with `--verbose` flag
- **Git Integration**: Works seamlessly with version control
- **Type Safety**: Pydantic models for data validation
- **Extensible Architecture**: Easy to add new commands and agents

## Technical Specifications

### Architecture
- **CLI Framework**: Typer (based on Click)
- **Terminal UI**: Rich
- **Data Models**: Pydantic v2
- **Template Engine**: Custom converter with 9 format types
- **Parser**: Custom markdown parser with regex-based extraction

### Dependencies
- Python >= 3.8
- typer[all] >= 0.9.0
- rich >= 13.0.0
- pyyaml >= 6.0.0
- pydantic >= 2.0.0
- pyfiglet >= 0.8.post1
- questionary >= 2.0.0

### Testing
- pytest + pytest-cov for testing and coverage
- Black (line length: 100) for code formatting
- isort for import sorting
- mypy for type checking

### Project Structure
```
stride/
├── cli.py                    # Main Typer app and command registration
├── models.py                 # Pydantic data models
├── constants.py              # Constants, enums, colors
├── utils.py                  # Utility functions (progress bars, formatting)
├── config.py                 # Configuration management
├── commands/                 # CLI command implementations
│   ├── init.py              # Project initialization
│   ├── list.py              # List sprints
│   ├── status.py            # Project status
│   ├── show.py              # Sprint details
│   ├── validate.py          # Validation
│   └── metrics.py           # Analytics
├── core/                     # Business logic
│   ├── sprint_manager.py    # Sprint CRUD operations
│   ├── markdown_parser.py   # Markdown parsing
│   ├── agent_registry.py    # Agent configurations
│   ├── template_converter.py # Template format conversion
│   ├── validator.py         # Validation logic
│   ├── analytics.py         # Analytics engine
│   ├── metrics_calculator.py # Metrics computation
│   └── sprint_parser.py     # Sprint file parsing
└── templates/                # Template files
    ├── sprint_files/        # Sprint document templates
    ├── agent_commands/      # Agent slash command templates
    └── agents_docs/         # Agent documentation
```

## File Organization

- **One command per file**: Each CLI command in separate file
- **Business logic in core**: Managers, parsers, converters
- **Models separate**: All Pydantic models in models.py
- **Constants centralized**: All constants in constants.py
- **Templates organized**: Sprint docs, agent commands, agent docs

## What's NOT Included (Future Roadmap)

- Advanced configuration management (config.yaml)
- File manager utilities (direct file operations in commands)
- Database backend (file-based storage only)
- Web UI (CLI only)
- CI/CD integration (manual setup required)
- Plugin system (built-in agents only)

## Version History

### v1.0.0 (2024-12-08)
- Initial production release
- 20 AI agent integrations
- 6 CLI commands
- 10 agent slash commands
- Advanced markdown parsing
- Sprint analytics engine
- Beautiful terminal UI
- Comprehensive documentation

## Getting Started

```bash
# Install
pip install stride

# Initialize project
stride init

# Select your AI agents interactively
# Then use agent commands like /stride:init in your AI tool

# Monitor progress
stride list
stride status
stride show SPRINT-XXXXX

# Analyze sprints
stride metrics
stride validate
```

## Philosophy

Stride is built on three core principles:

1. **Agent-First Design** - AI agents do the work, humans provide direction
2. **Sprint-Based Methodology** - Structured workflow (Proposed → Active → Completed)
3. **Spec-Driven Development** - Everything documented in markdown

## Use Cases

- **Indie Hackers**: Ship features without losing context
- **Startup CTOs**: Align multiple AI tools (Cursor + Claude + etc.)
- **Enterprise Devs**: Trust AI in legacy repos with validation
- **AI-First Developers**: Track what agents implemented across sprints

## License

MIT License - See LICENSE file for details

## Support

- GitHub Issues: https://github.com/saranmahadev/Stride/issues
- Documentation: https://github.com/saranmahadev/Stride#readme
- Repository: https://github.com/saranmahadev/Stride
