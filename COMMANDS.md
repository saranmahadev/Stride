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
  - [move](#stride-move)
  - [validate](#stride-validate)
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
