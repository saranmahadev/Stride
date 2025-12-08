# Agent Commands

Slash commands that AI agents use to plan, implement, and document sprints.

---

## Overview

When you run `stride init` and select AI agents, Stride installs 10 slash commands for each agent. These commands guide the agent through the complete sprint workflow.

**Command Syntax:**

- **Cursor**: `/stride:init`
- **Claude Code**: Use command name `init` in slash menu
- **Windsurf**: `/stride:init`
- **Other agents**: See `AGENTS.md` for syntax

---

## `/stride:init`

**Purpose:** Create project spec and start first sprint

**When to use:** Beginning of project or new major feature

**What it does:**

1. Creates `project.md` at root level with:
   - Project overview
   - Tech stack
   - Goals and objectives
   - Architecture notes

2. Creates first sprint in `.stride/sprints/SPRINT-XXXXX/`:
   - `proposal.md` with problem statement
   - Acceptance criteria
   - Success metrics

3. Asks for your approval to proceed with planning

**Example usage:**

```
Human: /stride:init

Agent: I'll help you set up your Stride project. Let me start by understanding your project...

[Creates project.md]
[Creates SPRINT-A3F2E/proposal.md]
[Waits for approval to continue]
```

---

## `/stride:plan`

**Purpose:** Define sprint goals and break down into actionable tasks

**When to use:** After proposal is approved

**What it does:**

1. Creates `plan.md` with:
   - **Strides** (milestones) - numbered phases
   - **Tasks** - checkboxes under each stride
   - **Purpose** - why each stride matters
   - **Completion Definition** - when each stride is done
   - **Approach** - technical approach
   - **Risks** - potential issues

2. Optionally creates `design.md` with:
   - Architecture diagrams
   - API designs
   - Data models
   - Technical specifications

**Example structure:**

```markdown
## Stride 1: Database Schema

**Purpose:** Set up user authentication tables

**Tasks:**
- [ ] Create users table
- [ ] Create sessions table
- [ ] Add indexes

**Completion Definition:** All tables created and migrated
```

---

## `/stride:implement`

**Purpose:** Build features with real-time implementation tracking

**When to use:** During development

**What it does:**

1. Creates/updates `implementation.md` with timestamped logs:
   - Current stride being worked on
   - Tasks addressed
   - Decisions made
   - Code changes
   - Notes and observations

2. Checks off tasks in `plan.md` as completed

3. Updates acceptance criteria in `proposal.md`

**Log format:**

```markdown
### [2025-01-15 14:30] Stride 1: Database Schema

**Tasks Addressed:**
- Created users table with email, password_hash columns
- Added unique index on email

**Decisions:**
- Using bcrypt for password hashing
- Session timeout set to 7 days

**Changes:**
- Added `models/user.py`
- Created migration `001_create_users.py`
```

---

## `/stride:status`

**Purpose:** Check current sprint progress

**When to use:** Anytime during development

**What it shows:**

- Current sprint ID and title
- Overall progress percentage
- Strides completed vs remaining
- Next tasks to work on
- Acceptance criteria status

**Example:**

```
Agent: Current Sprint Status:

Sprint: SPRINT-A3F2E - Add User Authentication
Progress: 75% (6/8 tasks completed)

Completed Strides:
✓ Stride 1: Database Schema
✓ Stride 2: API Endpoints

In Progress:
○ Stride 3: Frontend Integration (1/3 tasks)

Next Tasks:
- [ ] Create login component
- [ ] Add authentication context
```

---

## `/stride:review`

**Purpose:** Validate work and gather feedback

**When to use:** Before completing sprint

**What it does:**

1. Reviews implementation against:
   - Acceptance criteria
   - Task completion
   - Code quality
   - Documentation

2. Identifies gaps or issues

3. Suggests improvements

4. Documents review notes

---

## `/stride:complete`

**Purpose:** Archive sprint and document learnings

**When to use:** When sprint is done

**What it does:**

1. Verifies all tasks completed

2. Creates `retrospective.md` with:
   - **What Worked Well** - Successes
   - **What Could Be Improved** - Areas for growth
   - **Learnings** - Key takeaways
   - **Action Items** - For future sprints
   - **Metrics** - Duration, completion rate

3. Marks sprint as COMPLETED

**Retrospective structure:**

```markdown
## What Worked Well
- Clean separation of concerns in API design
- TDD approach caught bugs early

## What Could Be Improved
- Should have added logging from start
- Need better error messages

## Learnings
- Bcrypt is slower than expected - consider caching
- Frontend auth state management is complex

## Action Items
- Add logging framework in next sprint
- Research auth state libraries
```

---

## `/stride:present`

**Purpose:** Generate sprint presentations

**When to use:** For demos or documentation

**What it does:**

- Creates presentation-ready summary
- Highlights key features
- Shows before/after
- Includes metrics

---

## `/stride:derive`

**Purpose:** Create new sprint from existing one

**When to use:** Similar features or iterations

**What it does:**

- Analyzes existing sprint
- Creates new sprint with similar structure
- Adapts to new requirements
- Maintains consistency

---

## `/stride:lite`

**Purpose:** Execute small changes without sprint files

**When to use:** Small bug fixes, styling tweaks, or config changes (< 50 lines)

**What it does:**

- Follows a lightweight 5-stage workflow (Talk → Plan → Confirm → Implement → Complete)
- Operates entirely within the chat (no sprint files created)
- Validates eligibility (must be < 50 lines, < 3 files, single concern)

---

## `/stride:feedback`

**Purpose:** Collect and organize feedback

**When to use:** During or after sprint

**What it does:**

- Captures feedback from stakeholders
- Organizes by category
- Links to relevant tasks
- Tracks action items

---

## Command Flow

**Typical Sprint Flow:**

```
1. /stride:init      → Create project + first sprint
2. /stride:plan      → Break down into strides/tasks
3. /stride:implement → Build features (repeat)
4. /stride:status    → Check progress (as needed)
5. /stride:review    → Validate work
6. /stride:complete  → Archive + retrospective
```

**Parallel Commands:**

- `/stride:feedback` - Anytime
- `/stride:status` - Anytime
- `/stride:present` - Anytime

---

## Best Practices

!!! tip "Always start with /stride:init"
    This sets up the context for all other commands

!!! tip "Use /stride:implement frequently"
    Log as you go, don't wait until end

!!! tip "Check /stride:status often"
    Keep track of progress

!!! tip "Don't skip /stride:complete"
    Retrospectives are valuable for learning

---

## Multi-Agent Workflows

**Using Multiple Agents:**

```
Cursor     → /stride:init, /stride:plan
Claude Code → /stride:implement (backend)
Windsurf   → /stride:implement (frontend)
Cursor     → /stride:review, /stride:complete
```

All agents read/write to the same markdown files, ensuring consistency.

---

## Next Steps

- [CLI Commands →](cli-commands.md) - Monitor from terminal
- [Sprint Lifecycle →](sprint-lifecycle.md) - Understand the workflow
