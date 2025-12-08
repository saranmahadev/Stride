# CLI Commands

Monitor and manage your sprints from the terminal.

---

## `stride init`

Initialize Stride in your project directory.

```bash
stride init
```

**What it does:**

- Creates `.stride/` directory structure
- Interactive agent selection (20 AI agents)
- Installs slash commands for selected agents
- Creates sprint templates
- Sets up `AGENTS.md` documentation

**Options:**

- `--force`, `-f` - Force re-initialization

**Example:**

```bash
$ stride init

Welcome to Stride!

Select AI Tools to configure:
  ✓ Cursor
  ✓ Claude Code
  ✓ Windsurf

✨ Stride project initialized successfully!
```

---

## `stride list`

List all sprints with their status.

```bash
stride list
```

**Output:**

```bash
┌─────────────┬──────────────────────────┬──────────┬─────────────┐
│ Sprint ID   │ Title                    │ Status   │ Created     │
├─────────────┼──────────────────────────┼──────────┼─────────────┤
│ SPRINT-A3F2E│ Add User Authentication  │ ACTIVE   │ 2 hours ago │
│ SPRINT-B7C9D│ Payment Integration      │ PROPOSED │ 1 day ago   │
│ SPRINT-C4E1F│ Dashboard Redesign       │ COMPLETED│ 1 week ago  │
└─────────────┴──────────────────────────┴──────────┴─────────────┘
```

**Status Colors:**

- **PROPOSED** (Yellow) - Planning phase
- **ACTIVE** (Blue) - Implementation in progress
- **COMPLETED** (Green) - Done with retrospective

---

## `stride status`

Show current project status and active sprints.

```bash
stride status
```

**Output:**

- Project overview
- Active sprints summary
- Progress bars
- Recent activity

**Example:**

```bash
$ stride status

Project Status
--------------
Active Sprints: 1
Proposed Sprints: 2
Completed Sprints: 5

Current Sprint: SPRINT-A3F2E
Title: Add User Authentication
Progress: ████████████░░░ 75% (6/8 tasks)
```

---

## `stride show`

Display detailed information about a specific sprint.

```bash
stride show SPRINT-XXXXX
```

**What it shows:**

- Sprint title and status
- Progress breakdown by stride
- Acceptance criteria status
- Recent implementation logs
- Task completion

**Example:**

```bash
$ stride show SPRINT-A3F2E

Sprint: SPRINT-A3F2E
Title: Add User Authentication
Status: ACTIVE

Progress: ████████████░░░ 75% (6/8 tasks)

Strides:
  [✓] Stride 1: Database Schema (3/3 tasks)
  [✓] Stride 2: API Endpoints (2/2 tasks)
  [○] Stride 3: Frontend Integration (1/3 tasks)

Acceptance Criteria: 2/3 completed
```

---

## `stride validate`

Validate project structure and sprint files.

```bash
stride validate
```

**What it checks:**

- `.stride/` directory exists
- Required files present
- Markdown format validity
- Sprint file completeness
- Template integrity

**Example:**

```bash
$ stride validate

✓ Project structure valid
✓ All sprint files present
✓ Markdown format correct
✓ Templates intact

No issues found!
```

---

## `stride metrics`

View sprint analytics and statistics.

```bash
stride metrics
```

**Options:**

- `--export json` - Export to JSON
- `--export csv` - Export to CSV
- `--sprint SPRINT-ID` - Metrics for specific sprint

**What it shows:**

- Sprint duration
- Completion rates
- Task distribution
- Process compliance
- Quality indicators
- Trend analysis

**Example:**

```bash
$ stride metrics

Sprint Analytics
----------------
Total Sprints: 8
Completed: 5 (62.5%)
Average Duration: 3.2 days
Task Completion Rate: 87%

Process Compliance: 95%
✓ Planning documents: 100%
✓ Implementation logs: 100%
✓ Retrospectives: 80%
```

---

## Common Usage Patterns

### Daily Workflow

```bash
# Morning: Check status
stride status

# Throughout day: Monitor progress
stride show SPRINT-XXXXX

# Evening: Review completed work
stride list
```

### Sprint Management

```bash
# Start new sprint
stride init  # if needed
# Then use agent: /stride:init

# Track progress
stride show SPRINT-XXXXX

# Validate quality
stride validate

# Complete sprint
# Use agent: /stride:complete
stride metrics
```

### Multi-Sprint Projects

```bash
# View all sprints
stride list

# Compare sprints
stride metrics

# Validate everything
stride validate
```

---

## Tips

!!! tip "Use tab completion"
    If you installed Typer completion, use tab to autocomplete sprint IDs

!!! tip "Combine with Git"
    ```bash
    stride validate && git commit -m "Sprint progress"
    ```

!!! tip "Export metrics regularly"
    ```bash
    stride metrics --export json > metrics.json
    ```

---

## Next Steps

- [Agent Commands →](agent-commands.md) - Learn agent slash commands
- [Sprint Lifecycle →](sprint-lifecycle.md) - Understand sprint workflow
