# Stride CLI Reference

Complete command-line reference for the Stride framework.

## Table of Contents

- [Global Options](#global-options)
- [Commands](#commands)
  - [init](#stride-init)
  - [create](#stride-create)
  - [list](#stride-list)
  - [status](#stride-status)
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

List sprints with filtering and formatting options.

**Usage:**
```bash
stride list [OPTIONS]
```

**Options:**

| Option | Short | Description |
|--------|-------|-------------|
| `--status` | `-s` | Filter by status (proposed, active, blocked, review, completed) |
| `--format` | `-f` | Output format: table (default), list, json |

**Examples:**

```bash
# List all sprints (table format)
stride list

# List only active sprints
stride list --status active

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

Validate sprint structure and metadata.

Checks that sprint folders contain required documents with valid frontmatter metadata.

**Usage:**
```bash
stride validate [SPRINT_ID] [OPTIONS]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--all` | Validate all sprints in the project |
| `--strict` | Enable strict validation (fails on warnings) |

**Examples:**

```bash
# Validate single sprint
stride validate SPRINT-7K9P

# Validate with strict mode
stride validate SPRINT-7K9P --strict

# Validate all sprints
stride validate --all

# Validate all with strict mode
stride validate --all --strict
```

**Output (Valid Sprint):**
```
✓ SPRINT-7K9P: User Authentication
  All required documents present
  Metadata valid
  Status folder matches declared status
```

**Output (Invalid Sprint):**
```
✗ SPRINT-7K9P: User Authentication
  ⚠ Missing required document: plan.md
  ⚠ Invalid metadata: missing 'priority' field
  ✓ Status folder matches declared status
```

**Validation Checks:**
- Required documents exist (proposal.md)
- Metadata format is valid YAML
- Required metadata fields present (id, title, status)
- Sprint ID format is correct (SPRINT-XXXX)
- Status value is valid
- Physical location matches declared status

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
