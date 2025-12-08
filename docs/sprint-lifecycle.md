# Sprint Lifecycle

Understanding how sprints flow from idea to completion.

---

## The Three Phases

Every sprint in Stride follows a simple lifecycle:

```
PROPOSED → ACTIVE → COMPLETED
```

**Status is determined by files that exist:**

- **PROPOSED**: `proposal.md` and/or `plan.md` exist
- **ACTIVE**: `implementation.md` exists
- **COMPLETED**: `retrospective.md` exists

---

## Phase 1: PROPOSED

**Duration:** Planning phase (usually hours to 1 day)

**Files Created:**

1. **`proposal.md`** - The "what" and "why"
   - Problem statement
   - Goals and objectives
   - Acceptance criteria (checkboxes)
   - Success metrics
   - Out of scope

2. **`plan.md`** - The "how"
   - Strides (numbered milestones)
   - Tasks (checkboxes under each stride)
   - Technical approach
   - Risks and mitigations
   - Dependencies

3. **`design.md`** (optional) - The technical details
   - Architecture diagrams
   - API designs
   - Data models
   - Component structure

**Agent Commands Used:**

- `/stride:init` - Creates proposal
- `/stride:plan` - Creates plan and optionally design

**Goal:** Fully plan the sprint before writing code

**Example Directory:**

```
.stride/sprints/SPRINT-A3F2E/
├── proposal.md    ← What we're building
├── plan.md        ← How we'll build it
└── design.md      ← Technical architecture
```

---

## Phase 2: ACTIVE

**Duration:** Implementation phase (days to weeks)

**Files Updated:**

1. **`implementation.md`** - Real-time development log
   - Timestamped entries
   - Current stride being worked on
   - Tasks addressed
   - Decisions made
   - Code changes
   - Notes and blockers

2. **`plan.md`** - Task checkboxes get marked as done
   - `- [ ]` → `- [x]`

3. **`proposal.md`** - Acceptance criteria updated
   - `- [ ]` → `- [x]`

**Agent Commands Used:**

- `/stride:implement` - Log progress, update tasks
- `/stride:status` - Check progress
- `/stride:review` - Validate work

**Goal:** Build the feature while documenting progress

**Example Implementation Log:**

```markdown
## Implementation Log

### [2025-01-15 10:00] Stride 1: Database Schema

**Tasks Addressed:**
- Created users table
- Added email uniqueness constraint

**Decisions:**
- Using bcrypt for passwords
- Email stored lowercase

**Changes:**
- Added models/user.py
- Migration 001_create_users.py

**Notes:**
- Bcrypt is slower than expected
- May need caching layer
```

---

## Phase 3: COMPLETED

**Duration:** Retrospective phase (30 minutes to 1 hour)

**Files Created:**

1. **`retrospective.md`** - Learnings and reflection
   - What worked well
   - What could be improved
   - Key learnings
   - Action items for next sprint
   - Metrics (duration, completion rate)

**Agent Command Used:**

- `/stride:complete` - Creates retrospective

**Goal:** Capture learnings for continuous improvement

**Example Retrospective:**

```markdown
## Sprint Retrospective

### What Worked Well
✓ TDD approach caught bugs early
✓ Clear acceptance criteria
✓ Good separation of concerns

### What Could Be Improved
- Should have added logging sooner
- Error messages could be clearer
- Need better documentation

### Learnings
- Bcrypt hashing is CPU-intensive
- Frontend state management is complex
- API design impacts frontend code

### Action Items
- [ ] Add logging framework next sprint
- [ ] Research auth state libraries
- [ ] Create API design checklist

### Metrics
- Duration: 3 days
- Tasks completed: 8/8 (100%)
- Acceptance criteria: 3/3 (100%)
```

---

## Visual Flow

```
┌─────────────┐
│   PROPOSED  │  Planning
│             │  - Define problem
│ proposal.md │  - Set goals
│ plan.md     │  - Design approach
│ design.md   │
└──────┬──────┘
       │ /stride:implement
       ▼
┌─────────────┐
│   ACTIVE    │  Implementation
│             │  - Write code
│ + implement.│  - Log progress
│   ation.md  │  - Update tasks
└──────┬──────┘
       │ /stride:complete
       ▼
┌─────────────┐
│  COMPLETED  │  Retrospective
│             │  - Document learnings
│ + retrospec-│  - Capture metrics
│   tive.md   │  - Action items
└─────────────┘
```

---

## File-Based State Machine

Stride uses **files as state indicators**:

```python
if retrospective.md exists:
    status = COMPLETED
elif implementation.md exists:
    status = ACTIVE
elif plan.md exists:
    status = PROPOSED
```

**Benefits:**

- No database needed
- Git tracks all changes
- Easy to understand
- Visible in file explorer

---

## Progress Tracking

### Strides (Milestones)

```markdown
## Stride 1: Database Schema
- [x] Create users table
- [x] Add indexes
- [x] Write migration

## Stride 2: API Endpoints
- [x] POST /auth/register
- [ ] POST /auth/login      ← Currently here
- [ ] POST /auth/logout
```

### Acceptance Criteria

```markdown
## Acceptance Criteria
- [x] Users can register with email/password
- [ ] Users can login and receive JWT token
- [ ] Users can logout and invalidate token
```

---

## Common Patterns

### Quick Iteration Sprint

```
Day 1 Morning:  /stride:init + /stride:plan
Day 1 Afternoon: /stride:implement
Day 2:          /stride:implement
Day 3 Morning:  /stride:review
Day 3 Afternoon: /stride:complete
```

### Large Feature Sprint

```
Week 1: Plan (detailed design)
Week 2-3: Implement (multiple strides)
Week 4: Review, refine, complete
```

### Bug Fix Sprint

```
Hour 1: /stride:init (describe bug)
Hour 2: /stride:plan (root cause + fix)
Hour 3: /stride:implement (fix + tests)
Hour 4: /stride:complete
```

---

## Multi-Sprint Projects

**Typical Structure:**

```
.stride/sprints/
├── SPRINT-A3F2E/  (COMPLETED) - Auth system
├── SPRINT-B7C9D/  (COMPLETED) - User profiles
├── SPRINT-C4E1F/  (ACTIVE)    - Payments
└── SPRINT-D2A8B/  (PROPOSED)  - Admin panel
```

**Progression:**

1. Foundation sprints first (auth, database)
2. Feature sprints build on foundation
3. Polish sprints at end (UI, performance)

---

## Best Practices

!!! tip "Keep sprints small"
    1-3 days is ideal. Break large features into multiple sprints.

!!! tip "Complete one before starting next"
    Finish retrospective before planning next sprint.

!!! tip "Use git commits"
    Commit after each phase:
    ```bash
    git add .stride/sprints/SPRINT-XXXXX
    git commit -m "Sprint XXXXX: Planning complete"
    ```

!!! tip "Archive old sprints"
    Move completed sprints to `.stride/archive/` after 6 months.

---

## Monitoring with CLI

```bash
# See all sprints and their phases
stride list

# Check active sprint progress
stride status

# Detailed view of specific sprint
stride show SPRINT-XXXXX

# Validate everything is correct
stride validate
```

---

## Next Steps

- [CLI Commands →](cli-commands.md) - Monitor sprints
- [Agent Commands →](agent-commands.md) - Work within sprints
- [Philosophy →](philosophy.md) - Why this workflow works
