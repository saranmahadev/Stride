# Stride CLI Reference

Complete command-line reference for the Stride framework.

## Table of Contents

- [Global Options](#global-options)
- [Commands](#commands)
  - [init](#stride-init)
  - [create](#stride-create)
  - [list](#stride-list)
  - [status](#stride-status)
  - [show](#stride-show)
  - [progress](#stride-progress)
  - [timeline](#stride-timeline)
  - [validate](#stride-validate)
  - [watch](#stride-watch)
  - [doctor](#stride-doctor)
  - [move](#stride-move)
  - [archive](#stride-archive)
  - [restore](#stride-restore)
  - [version](#stride-version)
- [Quick Start Guide](#quick-start-guide)
- [Sprint ID Format](#sprint-id-format)
- [Status Values](#status-values)
- [Output Formats](#output-formats)

---

## Global Options

These options can be used with any command:

| Option | Short | Description |
|--------|-------|-------------|
| `--verbose` | `-v` | Enable verbose output with detailed logging |
| `--quiet` | `-q` | Suppress non-essential output |
| `--help` | `-h` | Show help message and exit |

**Example:**
```bash
stride list --verbose
stride create --title "New Feature" --quiet
```

---

## Commands

### stride init

Initialize Stride in the current directory.

Creates the standard Stride folder structure for managing sprints across their lifecycle.

**Usage:**
```bash
stride init [OPTIONS]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--force` | Reinitialize even if already initialized |

**Examples:**

```bash
# Initialize Stride in current directory
stride init

# Force reinitialization
stride init --force
```

**Created Structure:**
```
sprints/
├── proposed/      # New sprint proposals
├── active/        # Actively being worked on
├── blocked/       # Blocked on external dependencies
├── review/        # Ready for review
├── completed/     # Successfully completed
└── archived/      # Archived sprints
```

---

### stride create

Create a new sprint with proposal document.

**Usage:**
```bash
stride create [OPTIONS]
```

**Options:**

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| `--title` | `-t` | ✓ | Sprint title (descriptive name) |
| `--id` | `-i` | ✗ | Custom sprint ID (auto-generated if not provided) |
| `--description` | `-d` | ✗ | Sprint description |
| `--tags` | | ✗ | Comma-separated tags (e.g., "feature,api,backend") |
| `--priority` | `-p` | ✗ | Priority level (low, medium, high, critical) |

**Examples:**

```bash
# Create sprint with auto-generated ID
stride create --title "Add user authentication"

# Create with custom ID
stride create --id SPRINT-AUTH --title "Add user authentication"

# Create with all options
stride create \
  --title "Add user authentication" \
  --description "Implement OAuth2 authentication flow" \
  --tags "feature,security,api" \
  --priority high

# Quiet mode (only show sprint ID)
stride create --title "Quick feature" --quiet
```

**Output:**
```
✓ Initialized sprint: SPRINT-7K9P
  Status: proposed
  Location: sprints/proposed/SPRINT-7K9P/
  
  Next steps:
    stride status SPRINT-7K9P          # View sprint details
    stride move SPRINT-7K9P active     # Start working on it
```

---

### stride list

List sprints with filtering, sorting, and formatting options.

**Usage:**
```bash
stride list [OPTIONS]
```

**Options:**

| Option | Short | Description |
|--------|-------|-------------|
| `--status` | `-s` | Filter by status (proposed, active, blocked, review, completed) |
| `--user` | `-u` | Filter by author email (case-insensitive) |
| `--since` | | Filter sprints created since date (YYYY-MM-DD) |
| `--until` | | Filter sprints created until date (YYYY-MM-DD) |
| `--sort` | | Sort by: date, priority, status, author, title |
| `--format` | `-f` | Output format: table (default), list, json |

**Examples:**

```bash
# List all sprints (table format)
stride list

# List only active sprints
stride list --status active

# Filter by author
stride list --user alice@example.com

# Filter by date range
stride list --since 2025-01-01 --until 2025-12-31

# Sort by priority (critical > high > medium > low)
stride list --sort priority

# Sort by creation date (newest first)
stride list --sort date

# Combine filters: active sprints by specific user, sorted by priority
stride list --status active --user alice@example.com --sort priority

# List in simple list format
stride list --format list

# List as JSON for scripting
stride list --format json

# List completed sprints
stride list --status completed
```

**Output (Table Format):**
```
Sprint ID       Status      Title                    Priority    Tags
─────────────────────────────────────────────────────────────────────
SPRINT-7K9P     active      User Authentication      high        feature,security
SPRINT-3X8Y     proposed    Payment Integration      medium      feature,api
SPRINT-2M4N     review      Dashboard Redesign       low         ui,design
```

**Output (List Format):**
```
• SPRINT-7K9P: User Authentication (active)
• SPRINT-3X8Y: Payment Integration (proposed)
• SPRINT-2M4N: Dashboard Redesign (review)
```

**Output (JSON Format):**
```json
[
  {
    "id": "SPRINT-7K9P",
    "title": "User Authentication",
    "status": "active",
    "priority": "high",
    "tags": ["feature", "security"]
  },
  ...
]
```

---

### stride status

Show detailed information about a specific sprint.

**Usage:**
```bash
stride status <SPRINT_ID>
```

**Examples:**

```bash
# Show sprint status
stride status SPRINT-7K9P

# Verbose mode with additional details
stride status SPRINT-7K9P --verbose
```

**Output:**
```
Sprint: SPRINT-7K9P
Title: User Authentication
Status: active
Priority: high
Tags: feature, security
Description: Implement OAuth2 authentication flow

Created: 2024-01-15 10:30:00 UTC
Updated: 2024-01-15 14:22:00 UTC

Location: sprints/active/SPRINT-7K9P/

Documents:
  ✓ proposal.md
  ✓ plan.md
  ⊗ implementation.md (not started)
  ⊗ retrospective.md (not started)

Dependencies:
  • SPRINT-3X8Y: Payment Integration
  • SPRINT-2M4N: Dashboard Redesign
```

---

### stride show

Display complete sprint details with document viewer.

Shows sprint metadata and allows viewing of sprint documents with Rich markdown rendering.

**Usage:**
```bash
stride show <SPRINT_ID> [OPTIONS]
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `SPRINT_ID` | The sprint identifier (e.g., SPRINT-7K9P) |

**Options:**

| Option | Short | Description |
|--------|-------|-------------|
| `--file` | `-f` | View specific document: proposal, plan, design, implementation, retrospective |

**Examples:**

```bash
# Show complete sprint information
stride show SPRINT-7K9P

# View proposal document with markdown rendering
stride show SPRINT-7K9P --file proposal

# View plan document
stride show SPRINT-7K9P --file plan

# View design document
stride show SPRINT-7K9P --file design

# View implementation notes
stride show SPRINT-7K9P --file implementation

# View retrospective
stride show SPRINT-7K9P --file retrospective
```

**Output (without --file):**
```
============================================================
📋 Sprint Details: SPRINT-7K9P
============================================================

Title: User Authentication
Status: active 🚀
Author: alice@example.com
Priority: ⭐⭐⭐ high
Tags: feature, security

Created: 2025-01-15T10:30:00Z
Updated: 2025-01-15T14:22:00Z
Location: F:\Project\stride\sprints\active\SPRINT-7K9P

────────────────────────────────────────────────────────────
📂 Sprint Files:

  ✅ proposal.md (1.2 KB)
  ✅ plan.md (3.4 KB)
  ✅ design.md (5.1 KB)
  ⚠️  implementation.md (not found)
  ⚠️  retrospective.md (not found)

💡 Tip: Use --file <name> to view a specific file

============================================================
```

**Output (with --file proposal):**
```
============================================================
📋 Sprint Details: SPRINT-7K9P
============================================================

Title: User Authentication
Status: active 🚀
...

────────────────────────────────────────────────────────────
📄 Proposal:

[Beautiful markdown rendering with Rich library]
- Headers with proper formatting
- Code blocks with syntax highlighting
- Lists and checkboxes
- Tables
- Links and emphasis
============================================================
```

**Features:**
- 🎨 Rich markdown rendering with syntax highlighting
- 📊 File existence validation with size display
- ⚠️  Clear warnings for missing documents
- 🔍 Specific file viewing with `--file` option
- 🖥️  Automatic fallback to plain text for unsupported terminals

---

### stride progress

Display detailed sprint progress with task breakdown.

Analyzes proposal.md and tracks task completion progress.

**Usage:**
```bash
stride progress <SPRINT_ID>
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `SPRINT_ID` | The sprint to analyze (e.g., SPRINT-7K9P) |

**Examples:**

```bash
# View sprint progress
stride progress SPRINT-7K9P

# Check progress of blocked sprint
stride progress SPRINT-BLOCK
```

**Output:**
```
============================================================
📊 Sprint Progress: SPRINT-7K9P
============================================================

Title: User Authentication
Status: active 🚀
Author: alice@example.com
Priority: ⭐⭐⭐ high

Created: 2025-01-15T10:30:00Z
Updated: 2025-01-15T14:22:00Z

────────────────────────────────────────────────────────────
✅ Task Progress:

  [█████████████░░░░░░░] 65% (13/20 tasks)

  ✅ Set up authentication middleware
  ✅ Create user model
  ✅ Implement login endpoint
  ❌ Add password hashing
  ❌ Create registration flow
  ❌ Set up session management
  ❌ Add logout functionality

────────────────────────────────────────────────────────────
📈 Summary:

  Completed: 13 tasks
  Remaining: 7 tasks
  Total: 20 tasks
  Progress: 65%

============================================================
```

**Features:**
- 📊 Visual progress bar with percentage
- ✅ Task-by-task completion status
- 🎯 Automatic checkbox detection in proposal.md
- 📈 Summary statistics with counts

---

### stride timeline

Display complete sprint timeline with all events.

Shows chronological event history including creation, status changes, updates, and more.

**Usage:**
```bash
stride timeline <SPRINT_ID> [OPTIONS]
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `SPRINT_ID` | The sprint to view (e.g., SPRINT-7K9P) |

**Options:**

| Option | Short | Description |
|--------|-------|-------------|
| `--limit` | `-n` | Limit number of events shown (most recent) |

**Event Types:**

| Icon | Type | Description |
|------|------|-------------|
| 🎉 | created | Sprint creation |
| 🔄 | status_changed | Status transitions (proposed→active→review→completed) |
| ✏️ | updated | Metadata updates (title, priority, tags, etc.) |
| 📝 | file_modified | Document changes (proposal, plan, design, etc.) |
| 🚫 | blocked | Sprint blocked with reason |
| ✅ | unblocked | Sprint unblocked |
| 🎯 | completed | Sprint marked as completed |

**Examples:**

```bash
# View complete timeline
stride timeline SPRINT-7K9P

# Show only recent 5 events
stride timeline SPRINT-7K9P --limit 5

# View timeline of blocked sprint
stride timeline SPRINT-BLOCK -n 10
```

**Output:**
```
============================================================
📅 Sprint Timeline: SPRINT-7K9P
============================================================

Title: User Authentication
Status: review 🔍
Created: 2025-01-15 10:30:00

────────────────────────────────────────────────────────────
Event History (7 events):

  Time                      Event                Details
  ──────────────────────────────────────────────────────────
  2025-01-15 10:30:00       🎉 Created           Priority: high
  2025-01-15 10:35:00       🔄 Status Changed    proposed → active
  2025-01-15 14:20:00       📝 File Modified     Updated plan.md
  2025-01-16 09:00:00       🔄 Status Changed    active → blocked: 
                                                 Waiting for API docs
  2025-01-16 15:30:00       ✅ Unblocked         API documentation 
                                                 received
  2025-01-16 15:31:00       🔄 Status Changed    blocked → active
  2025-01-17 16:45:00       🔄 Status Changed    active → review

────────────────────────────────────────────────────────────
📊 Summary:

  Total Events: 7
  First Event: 2025-01-15 10:30:00
  Latest Event: 2025-01-17 16:45:00
  Sprint Age: 2 days

============================================================
```

**Features:**
- 📅 Complete chronological event history
- 🎨 Event icons for quick visual scanning
- 🔍 Detailed event metadata (reasons, priorities, etc.)
- ⏱️  Timestamp tracking for all activities
- 📊 Summary statistics with event counts
- 🎯 --limit option for recent events only
- 🖥️  Automatic fallback to plain text for unsupported terminals

---

### stride watch

Watch a sprint for real-time file changes with live display.

Monitors sprint folder and displays live updates when files are modified, created, deleted, or moved. Shows sprint status, file list, and event log in a split-panel terminal UI.

**Usage:**
```bash
stride watch <SPRINT_ID> [OPTIONS]
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `SPRINT_ID` | The sprint to watch (e.g., SPRINT-7K9P) |

**Options:**

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--interval` | `-i` | float | 1.0 | Refresh interval in seconds |

**Examples:**

```bash
# Watch sprint with default 1-second refresh
stride watch SPRINT-7K9P

# Watch with faster refresh (0.5 seconds)
stride watch SPRINT-A1B2 --interval 0.5

# Watch with slower refresh (2 seconds)
stride watch SPRINT-TIME -i 2.0
```

**Live Display:**
```
╭────────────────── 📡 Sprint Monitor ───────────────────╮
│   Sprint:  SPRINT-7K9P                                 │
│    Title:  User Authentication                         │
│   Status:  active                                      │
│ Watching:  stride\sprints\active\SPRINT-7K9P           │
╰────────────────────────────────────────────────────────╯
╭──────── 📁 Files ─────────╮╭──── 📋 Recent Events ─────╮
│  File               Size  ││ 14:32:15 ✏️ proposal.md   │
│  ✓ proposal.md    1.4 KB  ││ 14:30:22 ✨ plan.md       │
│  ✓ plan.md        892 B   ││ 14:28:10 ✏️ proposal.md   │
│  · design.md           -  ││                           │
│  · implementation…     -  ││                           │
│  · retrospective.…     -  ││                           │
│  · notes.md            -  ││                           │
╰───────────────────────────╯╰───────────────────────────╯
╭────────────────────────────────────────────────────────╮
│ Monitoring every 1.0s • Press Ctrl+C to stop           │
╰────────────────────────────────────────────────────────╯
```

**Tracked Files:**
- `proposal.md` - Sprint proposal document
- `plan.md` - Implementation plan
- `design.md` - Design specifications
- `implementation.md` - Implementation notes
- `retrospective.md` - Post-completion retrospective
- `notes.md` - General notes

**Event Icons:**

| Icon | Event Type | Description |
|------|-----------|-------------|
| ✏️ | modified | File content changed |
| ✨ | created | New file created |
| 🗑️ | deleted | File deleted |
| 📦 | moved | File moved/renamed |

**Features:**
- 🔄 Real-time file system monitoring with watchdog
- 📊 Live split-panel display (files + events)
- 📁 File size tracking with automatic updates
- 🎨 Color-coded event types for quick identification
- ⏱️  Timestamp tracking for all file changes
- 🔍 Automatic filtering of non-sprint files
- 📝 Event history (last 20 events)
- 🚫 Debouncing to prevent duplicate events
- ⌨️  Graceful Ctrl+C handling
- 🖥️  Rich terminal UI with panels and tables

**Use Cases:**
- Monitor active development in real-time
- Track AI agent file modifications
- Watch for unexpected file changes
- Verify implementation progress
- Debug file system issues
- Live code review sessions
- Team collaboration monitoring

**Performance:**
- Minimal CPU usage when idle
- Efficient file system watching
- Configurable refresh rate
- No file content reading (size only)
- Automatic cleanup on exit

**Note:** Press `Ctrl+C` to stop watching at any time.

---

### stride doctor

Comprehensive health check for Stride installation and project integrity.

Diagnoses installation status, project structure, sprint health, and configuration issues. Provides actionable fix suggestions and auto-repair capabilities. Outputs detailed reports in Rich (colored terminal), JSON (CI/CD), or plain text formats.

**Usage:**
```bash
stride doctor [OPTIONS]
```

**Options:**

| Option | Short | Type | Description |
|--------|-------|------|-------------|
| `--fix` | | flag | Attempt to auto-fix detected issues |
| `--verbose` | `-v` | flag | Show detailed check information |
| `--json` | | flag | Output results as JSON |

**Examples:**

```bash
# Run basic health check
stride doctor

# Run with detailed output
stride doctor --verbose

# Export health report as JSON for CI/CD
stride doctor --json > health-report.json

# Attempt auto-fix of detected issues
stride doctor --fix

# Verbose mode with auto-fix
stride doctor --verbose --fix
```

**Health Check Categories:**

1. **Installation** (3 checks)
   - Python version (requires 3.8+)
   - Stride framework version
   - Required dependencies installed

2. **Project Structure** (5 checks)
   - `stride/` folder initialized
   - `sprints/` directory exists
   - Status folders present (proposed, active, blocked, review, completed)
   - Optional folders (specs, introspection, archived)
   - `project.md` file exists

3. **Sprints** (4 checks)
   - Sprint count and distribution
   - `proposal.md` exists for all sprints
   - Metadata validity (id, title, status, created)
   - ID matches folder name
   - Status matches folder location

4. **Configuration** (4 checks)
   - User config exists (`~/.stride/config.yaml`)
   - Project config exists (`stride.config.yaml`)
   - Configs validate against schemas
   - AI agents configured

**Health Scoring:**

Health score is calculated as: `(passed + warnings × 0.5) / total × 100`

| Score | Grade | Description |
|-------|-------|-------------|
| 90-100 | Excellent | Project is in great shape |
| 75-89 | Good | Minor issues, mostly warnings |
| 60-74 | Fair | Some errors, needs attention |
| 40-59 | Poor | Multiple errors, action required |
| 0-39 | Critical | Severe issues, immediate action needed |

**Rich Output Example:**
```
🏥 Running Stride Health Check...

✅ Installation
   ✓ Python 3.12.4 installed
   ℹ Running from source (not installed via pip)
   ✓ All 7 dependencies installed

⚠️ Project Structure
   ✓ Stride initialized
   ✓ Sprint folders exist
   ✗ Specifications folder missing
     💡 Create directory: F:\Stride\stride\specs
   ✗ Introspection folder missing
     💡 Create directory: F:\Stride\stride\introspection

✅ Sprints
   ℹ Found 16 sprint(s)
   ✓ All sprints have proposal.md
   ✓ All sprint metadata valid
   ✓ All sprint IDs match folders

⚠️ Configuration
   ✓ User config valid (~/.stride/config.yaml)
   ✓ Project config valid (stride.config.yaml)
   ⚠ No agents configured
     💡 Add agents with: stride config set project.agents

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Health Score: 68/100 (Fair)

Total Checks: 16 | ✓ 10 | ⚠ 2 | ✗ 4

💡 5 issue(s) can be auto-fixed with --fix flag
```

**JSON Output Example:**
```json
{
  "health_score": 68,
  "health_grade": "Fair",
  "total_checks": 16,
  "passed": 10,
  "warnings": 2,
  "errors": 4,
  "checks": [
    {
      "category": "Installation",
      "check": "Python Version",
      "status": "pass",
      "message": "Python 3.12.4 installed",
      "details": "Minimum version 3.8 required",
      "fix_suggestion": null,
      "auto_fixable": false
    },
    {
      "category": "Project Structure",
      "check": "Specifications Folder",
      "status": "error",
      "message": "Specifications folder missing",
      "details": "Expected at: F:\\Stride\\stride\\specs",
      "fix_suggestion": "Create directory: F:\\Stride\\stride\\specs",
      "auto_fixable": true
    }
  ]
}
```

**Check Icons:**

| Icon | Status | Description |
|------|--------|-------------|
| ✓ | pass | Check passed successfully |
| ⚠ | warning | Non-critical issue detected |
| ✗ | error | Critical issue requires attention |
| ℹ | info | Informational message |

**Exit Codes:**

| Code | Meaning | CI/CD Usage |
|------|---------|-------------|
| 0 | No errors | Build can proceed |
| 1 | Errors found | Build should fail |

**Auto-Fixable Issues:**

The `--fix` flag can automatically repair:
- Missing project directories (specs, introspection, blocked, completed)
- Missing `project.md` file
- Invalid status folder locations (moves sprints)
- Metadata schema violations (adds missing fields)
- Configuration file formatting issues

**Use Cases:**

1. **Development:**
   ```bash
   # Quick health check before starting work
   stride doctor
   
   # Detailed diagnostics for troubleshooting
   stride doctor --verbose
   ```

2. **CI/CD Integration:**
   ```bash
   # Fail build if project unhealthy
   stride doctor || exit 1
   
   # Export health metrics
   stride doctor --json > metrics/health.json
   ```

3. **Deployment:**
   ```bash
   # Pre-deployment validation
   stride doctor --verbose
   
   # Auto-fix issues before deploy
   stride doctor --fix
   ```

4. **Troubleshooting:**
   ```bash
   # Diagnose project issues
   stride doctor --verbose
   
   # View fixable issues
   stride doctor | grep "auto-fixable"
   
   # Repair and verify
   stride doctor --fix && stride doctor
   ```

**Features:**
- 🏥 Comprehensive 16-point health check
- 📊 Intelligent health scoring (0-100)
- 🎨 Rich terminal UI with colors and icons
- 📄 JSON export for automation
- 🔧 Auto-fix detection and suggestions
- 🚨 Exit codes for CI/CD integration
- 📋 Detailed check descriptions
- 💡 Actionable fix recommendations
- 🔍 Verbose mode for deep diagnostics
- ⚡ Fast execution (< 1 second)

**Common Issues Detected:**
- Missing Python dependencies
- Outdated Python version
- Missing project folders
- Sprint metadata inconsistencies
- ID/status mismatches
- Invalid configuration files
- Missing required files
- Unconfigured AI agents

**Note:** The doctor command is non-destructive by default. Use `--fix` flag to apply repairs.

---

### stride agent

Manage AI agents for your Stride project.

Track which AI tools assist with development by configuring agents in your project. View available agents from the registry, add agents to your project, remove agents, and view detailed agent information.

**Usage:**
```bash
stride agent COMMAND [OPTIONS]
```

**Available Commands:**

| Command | Description |
|---------|-------------|
| `list` | List all available AI agents and show configured status |
| `add` | Add an AI agent to your project configuration |
| `remove` | Remove an AI agent from your project |
| `info` | Show detailed information about a specific agent |

---

#### stride agent list

List all available AI agents and show which are configured for your project.

**Usage:**
```bash
stride agent list [OPTIONS]
```

**Options:**

| Option | Type | Description |
|--------|------|-------------|
| `--json` | flag | Output results as JSON |

**Examples:**

```bash
# List all agents with visual status
stride agent list

# Export agent list as JSON
stride agent list --json
```

**Output Example:**
```
🤖 AI Agents
   1 configured • 7 available

 ✓ Claude (Anthropic)
   ID: claude
   Advanced AI with strong reasoning, coding, and analysis capabilities
   Website: https://claude.ai

 · GitHub Copilot
   ID: copilot
   AI pair programmer integrated directly into your IDE
   Website: https://github.com/features/copilot

 · ChatGPT (OpenAI)
   ID: chatgpt
   Versatile conversational AI for general tasks and coding
   Website: https://chat.openai.com
```

**JSON Output Example:**
```json
{
  "configured_count": 1,
  "available_count": 7,
  "agents": [
    {
      "id": "claude",
      "name": "Claude (Anthropic)",
      "description": "Advanced AI with strong reasoning, coding, and analysis capabilities",
      "website": "https://claude.ai",
      "configured": true
    }
  ]
}
```

---

#### stride agent add

Add an AI agent to your project configuration.

**Usage:**
```bash
stride agent add AGENT_ID [OPTIONS]
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `AGENT_ID` | The agent to add (e.g., claude, copilot) |

**Options:**

| Option | Short | Description |
|--------|-------|-------------|
| `--quiet` | `-q` | Suppress non-essential output |

**Examples:**

```bash
# Add Claude agent
stride agent add claude

# Add agent in quiet mode
stride agent add copilot --quiet

# Add with uppercase (case-insensitive)
stride agent add CLAUDE
```

**Available Agent IDs:**
- `claude` - Claude (Anthropic)
- `copilot` - GitHub Copilot
- `chatgpt` - ChatGPT (OpenAI)
- `gemini` - Gemini (Google)
- `cursor` - Cursor AI
- `windsurf` - Windsurf (Codeium)
- `custom` - Custom Agent (for your own AI tools)

**Output Example:**
```
✅ Added agent: Claude (Anthropic)
📋 Total configured agents: 1
```

**Validation:**
- Agent ID must exist in the registry
- Case-insensitive matching
- Duplicate additions are detected and reported
- Agent is persisted to `stride.config.yaml`

---

#### stride agent remove

Remove an AI agent from your project configuration.

**Usage:**
```bash
stride agent remove AGENT_ID [OPTIONS]
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `AGENT_ID` | The agent to remove (e.g., claude, copilot) |

**Options:**

| Option | Short | Description |
|--------|-------|-------------|
| `--quiet` | `-q` | Suppress non-essential output |

**Examples:**

```bash
# Remove Claude agent
stride agent remove claude

# Remove agent in quiet mode
stride agent remove copilot --quiet
```

**Output Example:**
```
✅ Removed agent: Claude (Anthropic)
📋 Remaining agents: 0
```

---

#### stride agent info

Show detailed information about a specific AI agent.

**Usage:**
```bash
stride agent info AGENT_ID
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `AGENT_ID` | The agent to show info for (e.g., claude, copilot) |

**Examples:**

```bash
# Show Claude agent details
stride agent info claude

# Show Copilot details
stride agent info copilot
```

**Output Example (Configured Agent):**
```
🤖 Claude (Anthropic)
=====================

ID: claude
Description: Advanced AI with strong reasoning, coding, and analysis capabilities
Website: https://claude.ai

Configured: ✓ Yes

💡 Remove with: stride agent remove claude
```

**Output Example (Not Configured):**
```
🤖 GitHub Copilot
=================

ID: copilot
Description: AI pair programmer integrated directly into your IDE
Website: https://github.com/features/copilot

Configured: ✗ No

💡 Add to project with: stride agent add copilot
```

**Agent Registry:**

| Agent ID | Name | Description | Use Case |
|----------|------|-------------|----------|
| `claude` | Claude (Anthropic) | Advanced AI with strong reasoning capabilities | Complex problem-solving, architecture, technical discussions |
| `copilot` | GitHub Copilot | AI pair programmer integrated into IDE | Real-time code completion, inline suggestions |
| `chatgpt` | ChatGPT (OpenAI) | Versatile conversational AI | Brainstorming, explanations, quick coding tasks |
| `gemini` | Gemini (Google) | Multimodal AI with analytical capabilities | Data analysis, multi-modal tasks, research |
| `cursor` | Cursor AI | AI-first code editor with context awareness | Full-project context coding, multi-file edits |
| `windsurf` | Windsurf (Codeium) | AI-powered IDE with agentic flow | Autonomous coding tasks, multi-step implementations |
| `custom` | Custom Agent | Add your own AI tool | Specialized or proprietary AI tools |

**Use Cases:**

1. **Agent Tracking:**
   ```bash
   # Track which AI tools help with your project
   stride agent add claude
   stride agent add copilot
   
   # See all configured agents
   stride agent list
   ```

2. **Team Coordination:**
   ```bash
   # Check which agents the team uses
   stride agent list
   
   # Get details about a specific agent
   stride agent info claude
   ```

3. **CI/CD Integration:**
   ```bash
   # Export agent configuration for automation
   stride agent list --json > agents.json
   
   # Validate agent configuration in build
   if stride agent list --json | grep -q '"configured": true'; then
     echo "Agents configured"
   fi
   ```

4. **Project Handoff:**
   ```bash
   # Document AI tools used in project
   stride agent list
   
   # Add recommended agents for new team members
   stride agent add claude
   stride agent add copilot
   ```

**Features:**
- 🤖 **7 Built-in Agents**: Pre-configured registry with major AI tools
- 🔍 **Agent Discovery**: Browse available agents and their capabilities
- 📋 **Configuration Tracking**: Persist agent selections in project config
- ✓ **Validation**: Verify agent IDs against registry
- 🎨 **Rich Display**: Visual status indicators (✓ configured, · not configured)
- 📄 **JSON Export**: Machine-readable output for automation
- 🔄 **Case-Insensitive**: Agent IDs work in any case
- 💡 **Actionable Hints**: Suggestions for adding/removing agents

**Configuration Storage:**

Agents are stored in `stride.config.yaml`:
```yaml
project:
  name: "My Project"
  agents:
    - claude
    - copilot
```

**Notes:**
- Agent configuration is project-specific (not user-level)
- Agents are tracked for attribution and documentation
- Custom agents allow integration of proprietary AI tools
- Agent info includes website links for more details

---

### stride export

Export sprint data for reporting and integration.

Supports multiple formats (JSON, Markdown, CSV, HTML) with comprehensive filtering options. Use filters to export specific sprints or `--all` for complete export.

**Usage:**
```bash
stride export [OPTIONS]
```

**Options:**

| Option | Short | Type | Description |
|--------|-------|------|-------------|
| `--format` | `-f` | choice | Export format: json, markdown, csv, html (default: markdown) |
| `--status` | `-s` | choice | Filter by status (can specify multiple) |
| `--since` | | date | Filter sprints created since date (YYYY-MM-DD) |
| `--until` | | date | Filter sprints created until date (YYYY-MM-DD) |
| `--user` | `-u` | text | Filter by author email |
| `--priority` | `-p` | choice | Filter by priority: critical, high, medium, low |
| `--tag` | `-t` | text | Filter by tag (can specify multiple) |
| `--agent` | `-a` | text | Filter by agent (can specify multiple) |
| `--output` | `-o` | path | Output file path (default: auto-generated) |
| `--all` | | flag | Export all sprints (no filters) |

**Examples:**

```bash
# Export all sprints as Markdown
stride export --all --format markdown

# Export completed sprints as JSON
stride export --format json --status completed --output completed.json

# Export high-priority sprints since January
stride export --format html --priority high --since 2025-01-01 --output high-priority.html

# Export sprints by specific author
stride export --format csv --user dev@example.com --output dev-sprints.csv

# Export sprints with multiple filters
stride export --status active --status review --tag feature --format markdown

# Export sprints by agent
stride export --agent claude --agent copilot --format json --output ai-assisted.json

# Export date range
stride export --since 2025-01-01 --until 2025-01-31 --format html --output january-2025.html
```

**Export Formats:**

#### JSON Format

Complete sprint data in structured JSON format. Ideal for programmatic processing, CI/CD integration, and data analysis.

**Structure:**
```json
{
  "export_metadata": {
    "timestamp": "2025-01-15T10:30:00Z",
    "total_sprints": 10,
    "exported_sprints": 5,
    "format": "json",
    "filters": {
      "status": ["completed"],
      "priority": "high"
    }
  },
  "sprints": [
    {
      "id": "SPRINT-7K9P",
      "status": "completed",
      "metadata": {
        "title": "User Authentication",
        "author": "dev@example.com",
        "priority": "high",
        "tags": ["feature", "security"],
        "agents": ["claude", "copilot"],
        "created": "2025-01-10T08:00:00Z",
        "updated": "2025-01-12T16:30:00Z"
      },
      "files": {
        "proposal.md": "# Proposal content...",
        "plan.md": "# Plan content...",
        "implementation.md": "# Implementation notes..."
      },
      "timeline": [
        {
          "event_type": "created",
          "timestamp": "2025-01-10T08:00:00Z"
        },
        {
          "event_type": "status_changed",
          "timestamp": "2025-01-10T09:00:00Z",
          "metadata": {
            "from_status": "proposed",
            "to_status": "active"
          }
        }
      ]
    }
  ]
}
```

**Use Cases:**
- CI/CD pipeline integration
- Automated reporting systems
- Data analysis and metrics
- Project management tool sync
- Backup and archival

#### Markdown Format

Human-readable reports with sprint summaries, statistics, and formatted metadata. Perfect for stakeholder reports and documentation.

**Features:**
- Sprint summaries with metadata tables
- Table of contents with clickable links
- Status and priority distribution statistics
- Timeline summaries
- File availability indicators

**Output Example:**
```markdown
# Sprint Export Report

**Generated:** 2025-01-15T10:30:00Z
**Format:** markdown
**Total Sprints:** 10
**Exported Sprints:** 5

## Filters Applied

- **Status:** completed
- **Priority:** high

## Table of Contents

1. [SPRINT-7K9P: User Authentication](#sprint-7k9p)
2. [SPRINT-AUTH2: OAuth Integration](#sprint-auth2)

## Sprint Summaries

### SPRINT-7K9P: User Authentication

| Field | Value |
|-------|-------|
| **ID** | SPRINT-7K9P |
| **Status** | completed |
| **Author** | dev@example.com |
| **Priority** | high |
| **Tags** | feature, security |
| **Agents** | claude, copilot |

**Files:**
- ✅ proposal.md (150 words)
- ✅ plan.md (300 words)
- ✅ implementation.md (500 words)

**Activity:** 8 events
```

**Use Cases:**
- Executive summaries
- Sprint retrospectives
- Documentation generation
- Stakeholder reports
- Project status updates

#### CSV Format

Tabular data export for spreadsheets and data analysis tools. Includes sprint metadata and file availability.

**Columns:**
- sprint_id
- status
- title
- author
- priority
- created
- updated
- tags (semicolon-separated)
- agents (semicolon-separated)
- description
- has_proposal (yes/no)
- has_plan (yes/no)
- has_design (yes/no)
- has_implementation (yes/no)
- has_retrospective (yes/no)
- event_count

**Example:**
```csv
# Sprint Export Report
# Generated: 2025-01-15T10:30:00Z
# Total Sprints: 10
# Exported Sprints: 5
sprint_id,status,title,author,priority,created,updated,tags,agents,has_proposal,has_plan,event_count
SPRINT-7K9P,completed,User Authentication,dev@example.com,high,2025-01-10T08:00:00Z,2025-01-12T16:30:00Z,feature;security,claude;copilot,yes,yes,8
```

**Use Cases:**
- Excel/Google Sheets analysis
- Data visualization tools
- Import into project management systems
- Bulk data processing
- Quick filtering and sorting

#### HTML Format

Styled web reports with interactive elements and embedded CSS. Beautiful reports for sharing and presentation.

**Features:**
- Responsive design
- Color-coded status badges
- Metadata cards
- Statistics tables
- Timeline visualization
- Embedded CSS styling
- Print-friendly layout

**Use Cases:**
- Team dashboards
- Client presentations
- Web-based reports
- Email attachments
- Archival documentation

**Filtering Options:**

#### Status Filtering

Filter by one or multiple sprint statuses:
```bash
# Single status
stride export --status completed

# Multiple statuses
stride export --status active --status review
```

**Available Statuses:** proposed, active, blocked, review, completed

#### Date Range Filtering

Filter by creation date range:
```bash
# Sprints since a date
stride export --since 2025-01-01

# Sprints until a date
stride export --until 2025-01-31

# Date range
stride export --since 2025-01-01 --until 2025-01-31
```

**Date Format:** YYYY-MM-DD

#### Author Filtering

Filter by author email (partial match):
```bash
stride export --user dev@example.com
stride export --user alice
```

#### Priority Filtering

Filter by priority level:
```bash
stride export --priority high
stride export --priority critical
```

**Available Priorities:** critical, high, medium, low

#### Tag Filtering

Filter by tags (any match):
```bash
# Single tag
stride export --tag feature

# Multiple tags (OR logic)
stride export --tag feature --tag security
```

#### Agent Filtering

Filter by configured AI agents (any match):
```bash
# Single agent
stride export --agent claude

# Multiple agents (OR logic)
stride export --agent claude --agent copilot
```

**Combining Filters:**

All filters can be combined for precise exports:
```bash
stride export \
  --format html \
  --status completed \
  --priority high \
  --since 2025-01-01 \
  --tag feature \
  --agent claude \
  --output high-priority-features.html
```

**Output File Naming:**

If `--output` is not specified, files are auto-generated:
- Format: `stride-export-YYYYMMDD-HHMMSS.{extension}`
- Example: `stride-export-20250115-103000.json`

**Integration Examples:**

#### CI/CD Pipeline

```yaml
# GitHub Actions example
- name: Export Sprint Data
  run: |
    stride export --format json --status completed --output build/sprints.json
    stride export --format html --all --output build/report.html
```

#### Reporting Script

```bash
#!/bin/bash
# Generate weekly sprint report

WEEK_START=$(date -d "last monday" +%Y-%m-%d)
WEEK_END=$(date -d "next sunday" +%Y-%m-%d)

stride export \
  --format markdown \
  --since $WEEK_START \
  --until $WEEK_END \
  --output "reports/week-$(date +%Y-%U).md"
```

#### Data Analysis

```python
import json
import subprocess

# Export sprint data
result = subprocess.run(
    ["stride", "export", "--format", "json", "--all"],
    capture_output=True,
    text=True
)

data = json.loads(result.stdout)

# Analyze data
for sprint in data["sprints"]:
    print(f"Sprint: {sprint['id']}")
    print(f"Events: {len(sprint['timeline'])}")
```

**Performance Notes:**

- Export time scales with number of sprints and file sizes
- Large exports (>100 sprints) may take several seconds
- JSON and CSV formats are fastest
- HTML format includes embedded styles (~10KB overhead)
- Filtering reduces export time by limiting sprints processed

**Error Handling:**

```bash
# Invalid date format
$ stride export --since 2025-13-40
❌ Invalid date format for --since: 2025-13-40 (use YYYY-MM-DD)

# Unknown format
$ stride export --format xml
❌ Unknown format: xml. Available: json, markdown, csv, html

# No sprints match filters
$ stride export --status completed --priority critical
📤 Exporting sprints...
✅ Export complete!
   Output: stride-export-20250115-103000.md
   Format: markdown
   Exported: 0 sprints (no matches found)
```

**Notes:**
- Export preserves all sprint data including metadata, files, and timeline
- File contents are included in JSON format for complete backup
- Filters use AND logic (all conditions must match)
- Multiple values for same filter use OR logic (any match)
- Export does not modify source sprints
- Output files are created with UTF-8 encoding
- Auto-generated filenames include timestamp to prevent overwrites

---

### stride move

---

### stride move

Move a sprint to a different status folder.

**Usage:**
```bash
stride move <SPRINT_ID> <STATUS> [OPTIONS]
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `SPRINT_ID` | The sprint to move (e.g., SPRINT-7K9P) |
| `STATUS` | Target status (proposed, active, blocked, review, completed) |

**Options:**

| Option | Description |
|--------|-------------|
| `--reason` | Reason for the status change |

**Examples:**

```bash
# Move sprint to active status
stride move SPRINT-7K9P active

# Move to blocked with reason
stride move SPRINT-7K9P blocked --reason "Waiting for API documentation"

# Move to review
stride move SPRINT-7K9P review --reason "Implementation complete"

# Mark as completed
stride move SPRINT-7K9P completed
```

**Output:**
```
✓ Moved SPRINT-7K9P: proposed → active
  Location: sprints/active/SPRINT-7K9P/
  Reason: Ready to start implementation
```

---

### stride validate

Comprehensive sprint quality validation with detailed reports.

Validates sprint structure, content quality, metadata completeness, and consistency across four categories.

**Usage:**
```bash
stride validate [SPRINT_ID] [OPTIONS]
```

**Options:**

| Option | Short | Description |
|--------|-------|-------------|
| `--all` | | Validate all sprints in the project |
| `--detailed` | `-d` | Show detailed validation report with categories |
| `--status` | `-s` | Filter sprints by status (active, review, completed, etc.) |
| `--strict` | | Enable strict validation (fails on warnings) |

**Validation Categories:**

1. **Structure**: File existence, unexpected files, required documents
2. **Content Quality**: Document length, section detection, code blocks, task checkboxes
3. **Metadata Completeness**: Required fields (id, title, status, created), recommended fields (author, priority, tags)
4. **Consistency**: Sprint ID matching, timestamp validation

**Examples:**

```bash
# Basic validation (summary only)
stride validate SPRINT-7K9P

# Detailed validation report with all checks
stride validate SPRINT-7K9P --detailed

# Validate all active sprints
stride validate --all --status active

# Detailed validation of all sprints
stride validate --all --detailed

# Validate with strict mode (warnings = errors)
stride validate SPRINT-7K9P --strict
```

**Output (Basic Mode):**
```
✓ SPRINT-7K9P

Summary: 1 valid, 0 invalid
```

**Output (Detailed Mode):**
```
✓ SPRINT-7K9P
  Checks: 22 | Passed: 16 | Warnings: 6 | Errors: 0

  Structure:
    ✓ proposal.md exists
    ⚠ plan.md not found (optional)
    ⚠ design.md not found (optional)

  Content_Quality:
    ✓ Proposal has adequate content (590 chars)
    ✓ Contains 'objective' section
    ✓ Contains 'scope' section
    💡 Suggestions:
      • Consider adding code examples to proposal

  Metadata:
    ✓ Required field 'id' present: SPRINT-7K9P
    ✓ Required field 'title' present: User Authentication
    ✓ Required field 'status' present: active
    ✓ Required field 'created' present
    ✓ Valid priority: high
    ⚠ Missing recommended field: tags

  Consistency:
    ✓ Sprint ID matches folder name
    ✓ Created timestamp is valid
```

**Output (Invalid Sprint):**
```
✗ SPRINT-BAD1
  Checks: 18 | Passed: 10 | Warnings: 2 | Errors: 6

  Structure:
    ✗ Missing proposal.md (REQUIRED)
    ✓ sprints/ folder exists

  Content_Quality:
    (No content to analyze)

  Metadata:
    ✗ Missing required field: id
    ✗ Missing required field: title
    ✗ Missing required field: status

  Consistency:
    ✗ Sprint ID does not match folder name
```

**Quality Checks:**

| Check | Category | Description |
|-------|----------|-------------|
| proposal.md exists | Structure | Validates required proposal document |
| Optional files | Structure | Warns if plan.md, design.md missing |
| Unexpected files | Structure | Identifies non-standard files |
| Content length | Content Quality | Minimum 100 chars (proposal), 50 (plan/design) |
| Section detection | Content Quality | Checks for objective, scope, requirements |
| Code blocks | Content Quality | Detects code examples |
| Task checkboxes | Content Quality | Counts `- [ ]` and `- [x]` tasks |
| Required fields | Metadata | id, title, status, created must exist |
| Recommended fields | Metadata | author, priority, tags should exist |
| Field validation | Metadata | Validates priority values, email format |
| ID matching | Consistency | Sprint ID matches folder name |
| Timestamp validation | Consistency | created/updated timestamps are valid |

**Actionable Suggestions:**

The validator provides suggestions for improvement:
- "Consider adding code examples to proposal"
- "Add plan.md to document implementation steps"
- "Set priority field (low/medium/high/critical)"
- "Add tags for better organization"
- "Include author field for team tracking"

---

### stride archive

Archive completed or cancelled sprints.

Moves sprints to the `sprints/archived/` folder for long-term storage.

**Usage:**
```bash
stride archive <SPRINT_ID> [OPTIONS]
```

**Options:**

| Option | Short | Description |
|--------|-------|-------------|
| `--reason` | `-r` | Reason for archiving |
| `--yes` | `-y` | Skip confirmation prompt |

**Examples:**

```bash
# Archive with confirmation
stride archive SPRINT-7K9P

# Archive with reason
stride archive SPRINT-7K9P --reason "Feature released to production"

# Archive without confirmation
stride archive SPRINT-7K9P --yes

# Archive with both options
stride archive SPRINT-7K9P --reason "No longer needed" --yes
```

**Output:**
```
⚠ This will archive SPRINT-7K9P: User Authentication
  Current status: completed
  Location: sprints/completed/SPRINT-7K9P/
  
Archive this sprint? [y/N]: y

✓ Archived SPRINT-7K9P
  Location: sprints/archived/SPRINT-7K9P/
  Reason: Feature released to production
```

---

### stride restore

Restore an archived sprint back to active development.

**Usage:**
```bash
stride restore <SPRINT_ID>
```

**Examples:**

```bash
# Restore archived sprint
stride restore SPRINT-7K9P

# With verbose output
stride restore SPRINT-7K9P --verbose
```

**Output:**
```
✓ Restored SPRINT-7K9P
  From: sprints/archived/SPRINT-7K9P/
  To: sprints/proposed/SPRINT-7K9P/
  
  Note: Sprint restored to 'proposed' status.
        Use 'stride move' to change status if needed.
```

---

### stride version

Show the current Stride version.

**Usage:**
```bash
stride version
# or
stride --version
```

**Output:**
```
stride, version 0.1.0
```

---

## Quick Start Guide

### 1. Initialize Stride

```bash
cd your-project
stride init
```

### 2. Create Your First Sprint

```bash
stride create \
  --title "Add user authentication" \
  --description "Implement OAuth2 flow with Google/GitHub" \
  --tags "feature,security" \
  --priority high
```

Output: `✓ Created: SPRINT-7K9P`

### 3. Start Working

```bash
# Move to active status
stride move SPRINT-7K9P active

# Check what needs to be done
stride status SPRINT-7K9P
```

### 4. Track Progress

```bash
# List all active sprints
stride list --status active

# Validate your work
stride validate SPRINT-7K9P
```

### 5. Complete the Sprint

```bash
# Mark as review
stride move SPRINT-7K9P review --reason "Implementation complete"

# After review, mark complete
stride move SPRINT-7K9P completed --reason "Passed review"
```

### 6. Archive When Done

```bash
# Archive completed sprint
stride archive SPRINT-7K9P --reason "Released to production" --yes
```

---

## Sprint ID Format

Sprint IDs follow a strict format for consistency:

- **Format:** `SPRINT-XXXX`
- **Pattern:** `SPRINT-` followed by 4+ uppercase alphanumeric characters
- **Valid Examples:**
  - `SPRINT-7K9P`
  - `SPRINT-AUTH`
  - `SPRINT-2024`
  - `SPRINT-FEATURE123`
- **Invalid Examples:**
  - `sprint-7k9p` (lowercase)
  - `SPRINT-abc` (only 3 characters)
  - `7K9P` (missing prefix)
  - `SPRINT_7K9P` (underscore instead of dash)

**Auto-generated IDs:** When you don't provide a custom ID, Stride generates a 4-character random code using:
- Uppercase letters (A-Z, excluding I and O to avoid confusion)
- Digits (2-9, excluding 0 and 1 to avoid confusion)

---

## Status Values

Sprints progress through these statuses:

| Status | Description | Typical Duration |
|--------|-------------|------------------|
| `proposed` | Initial proposal, awaiting approval | 1-2 days |
| `active` | Currently being worked on | 2-5 days |
| `blocked` | Blocked on external dependencies | Variable |
| `review` | Implementation complete, awaiting review | 1-2 days |
| `completed` | Approved and merged | Permanent |
| `archived` | Long-term storage for reference | Permanent |

**Status Flow:**
```
proposed → active → review → completed → archived
              ↓
            blocked → active
```

---

## Output Formats

### Table Format (Default)

Best for human-readable output in terminals.

```bash
stride list --format table
```

**Features:**
- Aligned columns
- Header row
- Colored output (when Rich is available)
- Sorted by status then ID

### List Format

Compact format for quick scanning.

```bash
stride list --format list
```

**Features:**
- One line per sprint
- Bullet points
- Status in parentheses
- Easy to grep/filter

### JSON Format

Machine-readable format for scripts and automation.

```bash
stride list --format json
```

**Features:**
- Valid JSON array
- All metadata included
- Perfect for piping to `jq` or other tools
- Parseable by any programming language

**Example with jq:**
```bash
# Get all active sprint IDs
stride list --format json | jq -r '.[] | select(.status == "active") | .id'

# Count sprints by status
stride list --format json | jq 'group_by(.status) | map({status: .[0].status, count: length})'
```

---

## Exit Codes

Stride uses standard exit codes for scripting:

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error (invalid arguments, file not found, etc.) |
| 2 | Validation failed (when using `--strict` mode) |

**Example Script:**
```bash
#!/bin/bash

# Validate all sprints, exit if any fail
if stride validate --all --strict; then
    echo "All sprints valid!"
    stride move SPRINT-7K9P review
else
    echo "Validation failed!"
    exit 1
fi
```

---

## Environment Variables

Currently, Stride uses minimal environment variables. Configuration is project-based.

Future releases will support:
- `STRIDE_CONFIG` - Path to custom config file
- `STRIDE_TEMPLATE_DIR` - Custom template directory
- `STRIDE_NO_COLOR` - Disable colored output

---

## Tips & Best Practices

### 1. Use Descriptive Titles

```bash
# Good
stride create --title "Add OAuth2 authentication with Google"

# Less helpful
stride create --title "Auth stuff"
```

### 2. Tag Consistently

Create a tagging convention for your project:

```bash
# Feature areas
--tags "frontend,backend,api,database"

# Categories
--tags "feature,bugfix,refactor,docs"

# Teams
--tags "team-core,team-platform,team-infra"
```

### 3. Use Priorities

```bash
# Critical: System down, data loss risk
--priority critical

# High: Important feature, major bug
--priority high

# Medium: Normal work items
--priority medium

# Low: Nice to have, technical debt
--priority low
```

### 4. Validate Often

```bash
# Before moving to review
stride validate SPRINT-7K9P

# Before committing
stride validate --all
```

### 5. Automate with Scripts

```bash
# Create sprint from issue tracker
create-sprint-from-issue() {
    local issue_id=$1
    local title=$(gh issue view $issue_id --json title -q .title)
    stride create --title "$title" --tags "github-issue-$issue_id"
}

# Auto-archive completed sprints
archive-completed() {
    stride list --status completed --format json \
        | jq -r '.[].id' \
        | xargs -I {} stride archive {} --yes --reason "Auto-archived"
}
```

---

## Getting Help

- **Command help:** `stride COMMAND --help`
- **General help:** `stride --help`
- **GitHub Issues:** [github.com/yourusername/stride/issues](https://github.com/yourusername/stride/issues)
- **Documentation:** [README.md](README.md)

---

*Generated for Stride v0.1.0*
