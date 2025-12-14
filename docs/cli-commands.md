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

## Team Collaboration (v1.5)

### `stride team init`

Initialize team collaboration configuration.

```bash
stride team init
```

**What it does:**

- Creates `.stride/team.yaml` file
- Configures approval policy (1 or 2 reviewers)
- Sets up team members
- Initializes workload tracking

**Interactive Configuration:**

```bash
$ stride team init

Team Initialization
-------------------
Approval Policy:
  1. Requires 1 approval
  2. Requires 2 approvals

Choose policy [1-2]: 2

Add team members? [y/N]: y

Member 1:
  Name: Alice
  Email: alice@example.com
  Role [developer/reviewer/lead]: lead

Member 2:
  Name: Bob
  Email: bob@example.com
  Role: developer

✨ Team configuration created!
```

**Options:**

- `--force`, `-f` - Overwrite existing configuration

---

### `stride team add`

Add a member to the team.

```bash
stride team add <name> <email> [--role ROLE]
```

**Arguments:**

- `name` - Member name (required)
- `email` - Member email (required)

**Options:**

- `--role`, `-r` - Role: developer, reviewer, or lead (default: developer)

**Example:**

```bash
$ stride team add "Charlie" "charlie@example.com" --role reviewer

✅ Added Charlie (charlie@example.com) as reviewer
```

---

### `stride team remove`

Remove a member from the team.

```bash
stride team remove <email>
```

**Example:**

```bash
$ stride team remove charlie@example.com

⚠️  This will unassign Charlie from all sprints.
Continue? [y/N]: y

✅ Removed charlie@example.com
```

---

### `stride team edit`

Edit member information.

```bash
stride team edit <email> [--name NAME] [--role ROLE]
```

**Options:**

- `--name`, `-n` - Update member name
- `--role`, `-r` - Update role (developer/reviewer/lead)

**Example:**

```bash
$ stride team edit bob@example.com --role lead

✅ Updated bob@example.com
```

---

### `stride team list`

List all team members with their roles and workloads.

```bash
stride team list
```

**Output:**

```bash
┌──────────────────────┬───────────┬───────────────┬──────────┐
│ Name                 │ Email     │ Role          │ Workload │
├──────────────────────┼───────────┼───────────────┼──────────┤
│ Alice                │ alice@... │ lead          │ 45       │
│ Bob                  │ bob@...   │ developer     │ 60       │
│ Charlie              │ charlie...│ reviewer      │ 30       │
└──────────────────────┴───────────┴───────────────┴──────────┘

Team Balance Score: 85/100
```

---

### `stride team show`

Show detailed information about a team member.

```bash
stride team show <email>
```

**Output:**

```bash
$ stride team show alice@example.com

Member: Alice
Email: alice@example.com
Role: lead

Assigned Sprints: 2
  • sprint-auth-refactor (Status: ACTIVE, Workload: 25)
  • sprint-api-endpoints (Status: PROPOSED, Workload: 20)

Total Workload: 45
Complexity Breakdown:
  High: 1 sprint
  Medium: 1 sprint
  Low: 0 sprints

Availability: Good
```

---

### `stride assign`

Assign a sprint to a team member (interactive with AI recommendations).

```bash
stride assign <sprint-id>
```

**What it does:**

- Analyzes current team workload
- Provides AI-scored recommendations
- Shows availability and complexity match
- Allows manual override

**Interactive Mode:**

```bash
$ stride assign sprint-auth-refactor

AI Assignee Recommendations
---------------------------
Sprint: sprint-auth-refactor
Workload: 25 | Complexity: Medium

Rank | Member  | Score | Reason
-----|---------|-------|-------
  1  | Alice   | 95    | Low current workload (20), expertise match
  2  | Bob     | 78    | Medium workload (45), available capacity
  3  | Charlie | 45    | High workload (60), limited availability

Select assignee [1-3] or enter email: 1

✅ Assigned sprint-auth-refactor to Alice
```

**Options:**

- `--direct <email>` - Skip AI recommendations, assign directly

---

### `stride assign direct`

Directly assign a sprint without AI recommendations.

```bash
stride assign direct <sprint-id> <email>
```

**Example:**

```bash
$ stride assign direct sprint-auth-refactor alice@example.com

✅ Assigned sprint-auth-refactor to alice@example.com
```

---

### `stride assign reassign`

Reassign a sprint to a different team member.

```bash
stride assign reassign <sprint-id> <new-email>
```

**Options:**

- `--reason TEXT` - Reason for reassignment

**Example:**

```bash
$ stride assign reassign sprint-auth alice@example.com --reason "Bob on PTO"

⚠️  Sprint currently assigned to bob@example.com
Reassigning to alice@example.com

✅ Reassigned sprint-auth-refactor
Reason: Bob on PTO
```

---

### `stride approve config`

Configure approval policy for the team.

```bash
stride approve config <policy>
```

**Arguments:**

- `policy` - Number of required approvals (1 or 2)

**Example:**

```bash
$ stride approve config 2

✅ Approval policy updated: Requires 2 approvals
```

---

### `stride approve`

Approve a sprint as a reviewer.

```bash
stride approve <sprint-id> [--comment TEXT]
```

**Options:**

- `--comment`, `-c` - Add approval comment

**Example:**

```bash
$ stride approve sprint-auth --comment "LGTM! Great work on error handling."

✅ Approval 1/2 recorded for sprint-auth
Reviewer: alice@example.com
Comment: LGTM! Great work on error handling.

Status: Pending (needs 1 more approval)
```

---

### `stride approve status`

Check approval status for a sprint.

```bash
stride approve status <sprint-id>
```

**Output:**

```bash
$ stride approve status sprint-auth

Sprint: sprint-auth-refactor
Policy: Requires 2 approvals

Approvals: 1/2
  ✓ alice@example.com (2024-12-14 10:30)
    "LGTM! Great work on error handling."

  ○ Pending from any reviewer

Status: ⚠️  Pending Approval
```

---

### `stride approve pending`

List all sprints pending your approval.

```bash
stride approve pending
```

**Output:**

```bash
$ stride approve pending

Pending Your Approval
---------------------

1. sprint-auth-refactor
   Assignee: bob@example.com
   Status: ACTIVE
   Approvals: 1/2
   Ready for review

2. sprint-api-endpoints
   Assignee: charlie@example.com
   Status: PROPOSED
   Approvals: 0/2
   Awaiting design review

Use: stride approve <sprint-id>
```

---

### `stride approve revoke`

Revoke your approval from a sprint.

```bash
stride approve revoke <sprint-id> [--reason TEXT]
```

**Options:**

- `--reason TEXT` - Reason for revocation

**Example:**

```bash
$ stride approve revoke sprint-auth --reason "Found security issue"

✅ Approval revoked for sprint-auth
Reason: Found security issue

New Status: 0/2 approvals
```

---

### `stride comment add`

Add a general comment to a sprint.

```bash
stride comment add <sprint-id> <text>
```

**Example:**

```bash
$ stride comment add sprint-auth "Don't forget to update the migration docs"

✅ Comment added to sprint-auth
Comment ID: c1
```

---

### `stride comment code`

Add a code-anchored comment to a sprint.

```bash
stride comment code <sprint-id> <file-path> <line-number> <text>
```

**Example:**

```bash
$ stride comment code sprint-auth src/auth.py 42 "Consider using bcrypt here"

✅ Code comment added to sprint-auth
File: src/auth.py:42
Comment ID: c2
```

---

### `stride comment reply`

Reply to an existing comment (threading).

```bash
stride comment reply <sprint-id> <comment-id> <text>
```

**Example:**

```bash
$ stride comment reply sprint-auth c2 "Good catch! Will update."

✅ Reply added to comment c2
Thread depth: 1
```

---

### `stride comment resolve`

Resolve a comment thread.

```bash
stride comment resolve <sprint-id> <comment-id>
```

**Example:**

```bash
$ stride comment resolve sprint-auth c2

✅ Resolved comment c2 and its 1 reply
```

---

### `stride comment list`

List all comments for a sprint.

```bash
stride comment list <sprint-id> [--unresolved]
```

**Options:**

- `--unresolved` - Show only unresolved comments

**Output:**

```bash
$ stride comment list sprint-auth

Comments for sprint-auth
------------------------

[c1] alice@example.com (2024-12-14 10:30)
"Don't forget to update the migration docs"
Status: Unresolved

[c2] alice@example.com (2024-12-14 10:35) [RESOLVED]
File: src/auth.py:42
"Consider using bcrypt here"
  └─ [c2-r1] bob@example.com (2024-12-14 10:40)
     "Good catch! Will update."

Total: 2 comments (1 unresolved)
```

---

### `stride comment stats`

Show comment statistics for a sprint.

```bash
stride comment stats <sprint-id>
```

**Output:**

```bash
$ stride comment stats sprint-auth

Comment Statistics
------------------
Total Comments: 5
Unresolved: 2
Resolved: 3

By Type:
  General: 3
  Code-anchored: 2

By Author:
  alice@example.com: 3
  bob@example.com: 2
```

---

## Enhanced Commands (v1.5)

### `stride list --assignee`

Filter sprints by assignee.

```bash
stride list --assignee <email>
```

**Example:**

```bash
$ stride list --assignee alice@example.com

┌─────────────┬──────────────────────────┬──────────┬──────────────┐
│ Sprint ID   │ Title                    │ Status   │ Assignee     │
├─────────────┼──────────────────────────┼──────────┼──────────────┤
│ SPRINT-A3F2E│ Add User Authentication  │ ACTIVE   │ alice@...    │
│ SPRINT-C4E1F│ Dashboard Redesign       │ COMPLETED│ alice@...    │
└─────────────┴──────────────────────────┴──────────┴──────────────┘
```

---

### `stride metrics` (Enhanced)

View workload and team balance metrics.

```bash
stride metrics --team
```

**Output:**

```bash
$ stride metrics --team

Team Workload Metrics
---------------------
Team Balance Score: 85/100

Member Workload:
  Alice:   45 (2 sprints) ████████░░
  Bob:     60 (3 sprints) ████████████
  Charlie: 30 (1 sprint)  ██████░░░░

Complexity Distribution:
  High:   2 sprints
  Medium: 3 sprints
  Low:    1 sprint

Recommendations:
  • Consider reassigning 1 sprint from Bob to Charlie
  • Team workload well-balanced overall
```

---

## Common Usage Patterns

### Team Setup Workflow

```bash
# Initialize team
stride team init

# Add members
stride team add "Alice" "alice@example.com" --role lead
stride team add "Bob" "bob@example.com" --role developer
stride team add "Charlie" "charlie@example.com" --role reviewer

# View team
stride team list
```

### Sprint Assignment Workflow

```bash
# Assign with AI recommendations
stride assign sprint-auth-refactor

# Or assign directly
stride assign direct sprint-auth-refactor alice@example.com

# Check workload balance
stride metrics --team

# Reassign if needed
stride assign reassign sprint-auth-refactor bob@example.com --reason "Better expertise match"
```

### Approval Workflow

```bash
# Check pending approvals
stride approve pending

# Approve a sprint
stride approve sprint-auth --comment "LGTM!"

# Check status
stride approve status sprint-auth

# Revoke if needed
stride approve revoke sprint-auth --reason "Found issue"
```

### Code Review Workflow

```bash
# Add code comment
stride comment code sprint-auth src/auth.py 42 "Consider using bcrypt"

# Add general comment
stride comment add sprint-auth "Great progress on tests!"

# Reply to comment
stride comment reply sprint-auth c1 "Thanks! Will address."

# Resolve comment
stride comment resolve sprint-auth c1

# View all comments
stride comment list sprint-auth

# View statistics
stride comment stats sprint-auth
```

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
