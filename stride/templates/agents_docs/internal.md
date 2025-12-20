# **Stride Instructions**

*Instructions for AI coding assistants using the Stride Framework for Sprint-Powered, Spec-Driven Development.*

> **IMPORTANT**
> AI agents MUST follow this instruction file strictly.
> All work MUST be triggered through Stride commands only.
> Agents MUST NOT modify sprint files outside their authorized phase.
> Each sprint file MUST follow its template exactly—no added or removed sections.
> Strides MUST be used exactly as defined below.

---

# **TL;DR Quick Checklist**

### **Lifecycle Commands**

| Command             | Phase                  | Files Allowed                               |
| ------------------- | ---------------------- | ------------------------------------------- |
| `/stride-init`      | Project Initialization | `.stride/project.md`                        |
| `/stride-derive`    | Sprint Discovery       | **Read-only**                               |
| `/stride-lite`      | Lightweight Changes    | Chat-only (no sprint files)                 |
| `/stride-status`    | Status Analysis        | **Read-only**                               |
| `/stride-plan`      | Sprint Planning        | `proposal.md`, `plan.md`, `design.md`       |
| `/stride-present`   | Approval Phase         | **Read-only**                               |
| `/stride-implement` | Implementation         | `implementation.md` (append-only)           |
| `/stride-feedback`  | Mid-sprint Adjustments | `plan.md`, `design.md`, `implementation.md` |
| `/stride-review`    | Validation             | **Read-only**                               |
| `/stride-complete`  | Finalization           | `retrospective.md`                          |

### **Human CLI**

* `stride list` — List sprints
* `stride show sprint-XYZ` — Display sprint details
* `stride status sprint-XYZ` — Show sprint phase
* `stride validate sprint-XYZ` — Run quality gates

### **NICE Marker System**

This project uses the NICE (Navigation and Intent Context Engine) marker system.
**You MUST read and understand `.stride/marker.md` before writing any code.**
All significant code blocks (ENTRY, LOGIC, IO, etc.) MUST be annotated with NICE markers.

---

# **1. Stride Workflow Overview**

Stride follows a **strict, file-governed, state-driven** 6-phase lifecycle.

Sprint folder structure:

```
.stride/sprints/
  sprint-[name]/
    proposal.md
    plan.md
    design.md
    implementation.md
    retrospective.md
```

### **Agents MUST follow this sequence strictly:**

1. **Init** → Establish project context
2. **Plan** → Create proposal + plan + optional design
3. **Present** → Wait for explicit approval
4. **Implement** → Execute Strides sequentially
5. **Review** → Validate outputs
6. **Complete** → Finalize & reflect

### **Global Behavioural Rules**

* ❗ Never modify a file outside its allowed phase
* ❗ Never alter folder structure
* ❗ Never revise old implementation logs (append-only)
* ❗ Never add/remove top-level sections inside templates
* ✔ Follow templates exactly
* ✔ Preserve separation between proposal → plan → design → implementation

---

# **1.1 What Are Strides? (Canonical Definition)**

A **Stride** is a **phase-level execution unit** inside a sprint.
It sits *between* the sprint and the tasks:

```
Sprint
 ├─ Stride 1 (Milestone)
 │    ├─ Task 1.1
 │    ├─ Task 1.2
 │    └─ Task 1.3
 ├─ Stride 2 (Milestone)
 │    ├─ Task 2.1
 │    └─ Task 2.2
 └─ Stride 3 (Milestone)
      ├─ Task 3.1
      └─ Task 3.2
```

### **Definition**

A **Stride** is a *logical, reviewable milestone* within a sprint that:

* Produces a tangible outcome
* Groups several related tasks
* Moves the sprint from one capability stage to the next
* Must be executed **sequentially**
* Must appear in `plan.md`
* Must appear in implementation logs
* Must be referenced in the retrospective

### **Rules for Strides**

1. **Sequential** — Strides MUST be completed in order.
2. **Outcome-Based** — Each Stride MUST deliver a meaningful system milestone.
3. **Traceable** — Every Stride MUST map 1:1 to implementation logs.
4. **Stable After Approval** — Strides only change via `/stride-feedback`.
5. **Testable** — Each Stride MUST satisfy at least one acceptance criterion.
6. **Distinct From Tasks** — Tasks are atomic actions; Strides are milestone bundles.

---

# **1.2 The NICE Marker System**

### **Concept**
The **NICE** (Name, Intent, Context, Example) Marker System allows agents to semantically annotate code to generate live documentation and specifications. This replaces stale external documentation with code-resident truth.

### **Syntax**
Markers are comment blocks in the code:

```python
# @intent <TYPE> <ID>
# @desc Description of what this block does
# @inputs param1: type, param2: type
# @outputs return_type
# @end
def my_function():
    ...
```

**Common Types:** `ENTRY`, `FLOW`, `LOGIC`, `TRANSFORM`, `IO`, `MODEL`.

### **Distributed SPEC Architecture**
Instead of one giant spec file, Stride uses a distributed approach:
1. **Root `SPEC.md`**: Located in project root. Acts as a map/index.
2. **Module `SPEC.md`**: Located in each subdirectory (e.g., `stride/core/SPEC.md`). Contains detailed specs for that module.

### **Agent Behaviour**
* **Read**: Use `stride marker view` to explore the codebase semantically.
* **Write**: Add markers when writing new code.
* **Update**: Run `stride annotate` to regenerate `SPEC.md` files after changes.

### **Enforcement**
**MANDATORY CHECKPOINT**: After completing each Stride during implementation:
1. Update all NICE markers for code changes
2. Regenerate affected SPEC.md files (module-level and root if needed)
3. Log markers and SPEC files in implementation entry
4. **Cannot proceed to next Stride without completing 1-3**

Empty or missing "NICE Markers Added" / "SPEC.md Files Updated" sections in logs are blocking issues.

---

# **1.3 Global Learnings System**

### **Concept**
`.stride/learnings.md` is the project's collective memory. It prevents repeating mistakes and promotes successful patterns.

### **Structure**
The file is organized by categories:
* **Architecture**: System-level decisions.
* **Patterns**: Preferred coding styles and idioms.
* **Gotchas**: Known issues and anti-patterns.
* **Workflow**: Process improvements.

### **Agent Behaviour**
1. **Check Existence**: Always verify `.stride/learnings.md` exists before reading/writing.
2. **If Missing**: 
   - Copy `.stride/templates/learnings.md` to `.stride/learnings.md`
   - Seed with **first learning entry** from project context (`.stride/project.md`)
   - Example first entry:
     ```markdown
     ## Architecture
     - [Project: {name}] Tech stack: {stack}. Architecture: {pattern}. (sprint-init)
     ```
3. **Before Planning**: Read `learnings.md` to avoid past pitfalls.
4. **During Feedback/Review**: Capture critical insights and append to `learnings.md`.
5. **During Retrospective**: Extract new lessons and append them to `learnings.md`.

---

# **2. Project Context (`/stride-init`)**

### **Goal**

Establish `.stride/project.md` as the **source-of-truth** for all sprints.

### **Agent Behaviour**

1. Check if `.stride/project.md` exists.
2. If missing → derive from repo or ask user for missing info.
3. Populate strictly using `.stride/templates/project.md`.
4. Planning cannot begin until this file is complete.

### **Rules**

`.stride/project.md` defines:

* Boundaries & scope
* Testing expectations
* Architectural conventions
* Coding standards
* Validation requirements
* Risks & assumptions

Agents MUST consult this file before every sprint.

---

# **3. Sprint Planning (`/stride-plan`)**

### **Goal**

Create a complete, reviewable sprint contract **before** coding begins.

### **Agent Behaviour**

1. Create:

```
.stride/sprints/sprint-[SHORTNAME]/
```

**SHORTNAME rules:**

* 4–12 chars
* Human readable
* Domain-relevant
* Unique

2. Generate the 3 planning files using template sources in `.stride/templates/`.

---

## **3.1 proposal.md**

Template Source: `.stride/templates/proposal.md`

Purpose: Define **intent, problem, boundaries, acceptance**.

Rules:

* High-level only
* NO architecture
* NO tasks
* Acceptance criteria MUST be measurable

---

## **3.2 plan.md**

Template Source: `.stride/templates/plan.md`

Purpose: Convert intent into:

* **Strides** (execution milestones)
* **Tasks** (atomic units)
* **Approach**
* **Risks**

Rules:

* Strides MUST be sequential & outcome-driven
* Tasks MUST map to implementation logs
* No code allowed

---

## **3.3 design.md** *(only if required)*

Template Source: `.stride/templates/design.md`

Rules:

* Required for architecture, APIs, data models, security, or cross-module changes
* Must capture decisions & trade-offs
* MUST remain aligned with `.stride/project.md`
* No implementation details

---

# **4. Presentation Phase (`/stride-present`)**

### **Goal**

Obtain explicit approval before implementation.

### **Agent Behaviour**

* Summarize proposal, plan, design
* Present Strides clearly
* Ask:
  **“Approve to proceed?”**

### **Rules**

* Read-only phase
* No implementation may begin without approval

---

# **5. Implementation Phase (`/stride-implement`)**

### **Goal**

Execute Strides and document work accurately.

### **Agent Behaviour**

* Execute Strides in strict order
* For each atomic change → append to `implementation.md`

### **Template Source:** `.stride/templates/implementation.md`

Rules:

* Append-only
* Each log must correspond to a Stride and its tasks
* Logs must be:
  * Factual
  * Chronological
  * Linked to deliverables
* Code changes must be summarized, not dumped

---

# **6. Feedback Phase (`/stride-feedback`)**

### **Goal**

Apply mid-sprint corrections safely and update project context if major changes discovered.

### **Agent Behaviour**

1. Pause implementation
2. Append "Feedback Received" to implementation log
3. Update:
   * `plan.md` (Strides & tasks)
   * `design.md` (if architecture changed)
4. **Check for Project-Level Impact** (Conditional)
   
   If feedback reveals changes that affect project-wide understanding, update `.stride/project.md` immediately:
   
   **Update project.md when feedback includes:**
   - New technical constraints discovered
   - Architecture patterns that should be standardized across project
   - Domain knowledge that generalizes beyond this sprint
   - Risk assumptions proven incorrect
   - Security or compliance requirements changed
   - Performance characteristics that affect project expectations
   
   **Sections most likely to need updates:**
   - Section 7: Domain Knowledge (entities, rules, relationships)
   - Section 8: Constraints (technical, business, operational)
   - Section 11: Risks & Assumptions (validations, new risks)
   
   **Process:**
   - Read current `.stride/project.md`
   - Identify which section(s) need updates
   - Append new learnings (preserve existing content)
   - Use format: `- [Description] (sprint-[NAME]): [Details]`
   - Log the project.md change in `implementation.md` under "Changes Applied"

5. Resume implementation

Rules:

* Must preserve original intent unless user says otherwise
* Must not violate acceptance criteria
* Project.md updates must be factual and traceable to this sprint

---

# **7. Review Phase (`/stride-review`)**

### **Goal**

Validate sprint output before completion.

### **Agent Behaviour**

Validate against:

* proposal.md
* plan.md
* design.md
* `.stride/project.md`
* All acceptance criteria

Run checks on:

* Code quality
* Tests
* Architecture alignment
* Documentation completeness

Rules:

* Entire phase is read-only
* Must list discrepancies
* Fixes require `/stride-feedback`

---

# **8. Completion Phase (`/stride-complete`)**

### **Goal**

Finalize sprint, produce learnings, and update project context based on insights.

### **Agent Behaviour**

1. **Review Sprint Learnings**
   - Analyze `implementation.md` for insights gained during sprint
   - Identify if any learnings affect project-wide context
   
2. **Update `.stride/project.md` (Conditional)**
   
   If sprint revealed project-level insights, update relevant sections:
   
   **Common scenarios requiring updates:**
   - Domain entities or business rules discovered → Update Section 7
   - New library restrictions or version requirements → Update Section 8.1
   - Performance benchmarks measured → Update Section 3.1
   - Security patterns established → Update Section 3.3
   - Operational constraints identified → Update Section 8.3
   - Assumptions validated or invalidated → Update Section 11
   
   **How to update:**
   - Read current section content
   - Append new learnings (don't delete existing content)
   - Use format: `- [Description] (sprint-[NAME]): [Details]`
   - Be specific and factual
   
3. **Generate `retrospective.md`**
   - Use template from `.stride/templates/retrospective.md`
   - Complete all sections including "Project Context Updates"
   - Reference specific Strides and decisions made
   - Document all project.md changes in "Project Context Updates" section
   
4. **Mark sprint as complete**
   - Provide final summary in chat
   - List project.md sections updated (if any)

Rules:

* No new tasks added here
* Retrospective MUST reference each Stride
* All project.md updates must be documented in retrospective

---

# **9. CLI Commands (Human Tools)**

Agents may interpret CLI output but must **not** simulate or modify CLI.

| Command                    | Description           |
| -------------------------- | --------------------- |
| `stride init`              | Initialize `.stride/` |
| `stride list`              | List sprints          |
| `stride show <sprint>`     | Show sprint summary   |
| `stride status <sprint>`   | Show lifecycle state  |
| `stride validate <sprint>` | Verify completeness   |

Validation checks include:

* Required files exist
* Strides completed
* Logs present & consistent
* No TODOs left
* Acceptance criteria satisfied

---

# **10. When to Use Stride Commands**

This section defines exactly **when each Stride command should be invoked**.
Agents MUST follow this strictly.

---

## **10.1 When to Use `/stride-init`**

### Use `/stride-init` for:

* First-time project setup
* Missing `.stride/project.md`
* Significant project structure changes
* Major technology, architecture, or domain pivots
* When context appears outdated or incomplete

### NOT for `/stride-init`:

* Minor cleanup
* Localized refactors
* Small code adjustments
* New sprints within an already initialized project

---

## **10.2 When to Use `/stride-derive`**

### Use `/stride-derive` for:

* Starting a new development phase
* Need sprint ideas or priorities
* Identifying technical debt opportunities
* Planning sprint backlog
* Discovering gaps in test coverage, documentation, or error handling
* Finding quick wins or high-impact improvements
* User asks: "What should we work on next?"

### NOT for `/stride-derive`:

* When user already knows the sprint they want (use `/stride-plan` directly)
* During active sprint implementation
* When project is not initialized (run `/stride-init` first)
* For status checking (use `/stride-status`)

---

## **10.3 When to Use `/stride-lite`**

### Use `/stride-lite` for:

* Bug fixes (< 50 lines)
* Styling or formatting adjustments
* Documentation edits
* Configuration changes
* Typo corrections
* Small refactors (single concern)
* Quick fixes that don't require architecture decisions

### NOT for `/stride-lite`:

* New features
* Architecture changes
* Multi-file refactors (> 3 files or > 50 lines)
* Security updates
* Changes requiring design decisions
* Anything that would need design.md

---

## **10.4 When to Use `/stride-status`**

### Use `/stride-status` for:

* User asks about project progress or health
* Need context on what's blocking work
* Understanding which sprint to focus on
* Deciding what needs attention
* User asks "How's it going?" or "What's the status?"
* Want overview before planning next steps

### NOT for `/stride-status`:

* During focused implementation work (don't distract)
* When creating new sprints (use `/stride-plan`)
* For quick file checks (not needed)
* Mid-implementation (stay focused)

---

## **10.5 When to Use `/stride-plan`**

### Use `/stride-plan` for:

* New features
* Architecture changes
* Security updates
* Data model changes
* Multi-module changes
* Broad refactors

### NOT for `/stride-plan`:

* Bug fixes
* Typos
* Document edits
* Formatting
* CI tweaks

---

## **10.6 When to Use `/stride-present`**

### Use `/stride-present` for:

* When the sprint is fully planned
* After `proposal`, `plan`, and `design` (if needed) are created
* Before any implementation begins
* When user approval is required

### NOT for `/stride-present`:

* During implementation
* Before planning is complete
* After feedback has already changed the plan (use present again only if required)

---

## **10.7 When to Use `/stride-implement`**

### Use `/stride-implement` for:

* Executing tasks defined in `plan.md`
* Working on Strides sequentially
* Performing write operations
* Updating `implementation.md`

### NOT for `/stride-implement`:

* Planning or redesigning
* Architectural decision-making
* Fixing sprint structure
* Producing or editing proposal/plan/design

---

## **10.8 When to Use `/stride-feedback`**

### Use `/stride-feedback` for:

* Mid-sprint corrections
* Adjusting Strides or tasks
* Updating `plan.md` when user requirements evolve
* Updating `design.md` due to new constraints
* Logging user feedback events in `implementation.md`

### NOT for `/stride-feedback`:

* Initial planning
* Completing tasks
* Final validation
* Retrospective editing

---

## **10.9 When to Use `/stride-review`**

### Use `/stride-review` for:

* Validating work before sprint completion
* Checking compliance with acceptance criteria
* Reviewing code quality, tests, and documentation
* Running a final internal audit

### NOT for `/stride-review`:

* Making modifications
* Adding new work
* Creating or adjusting tasks
* Writing implementation logs

---

## **10.10 When to Use `/stride-complete`**

### Use `/stride-complete` for:

* When ALL Strides are completed
* After `/stride-review` passes
* Generating the retrospective
* Marking the sprint as finished

### NOT for `/stride-complete`:

* If tasks remain incomplete
* If acceptance criteria are unmet
* If design or plan changed without review
* If validation fails

---

Agents MUST automatically choose commands based on **intent cues** in natural language.

### Triggers for `/stride-init`

* "Start the project"
* "Initialize Stride"
* "Set up the structure"

### Triggers for `/stride-derive`

* "Derive sprint ideas"
* "What should we work on next?"
* "Show me potential sprints"
* "Suggest sprint backlog"
* "What needs to be done?"
* "Help me prioritize work"
* "Analyze the codebase for tasks"

### Triggers for `/stride-lite`

* "Quick fix for..."
* "Small change to..."
* "Lite mode: [description]"
* "Just need to fix..."
* "Typo in..."
* "Update styling for..."
* "Change config..."
* "Fix this bug (it's small)"

### Triggers for `/stride-status`

* "How's the project going?"
* "What's the status?"
* "Show me project health"
* "Any blockers?"
* "What needs attention?"
* "Which sprint should I focus on?"
* "Give me an update"
* "Project status"

### Triggers for `/stride-plan`

* “Plan this feature”
* “Create a sprint”
* “Let’s build X”
* “Help me design a change”

### Triggers for `/stride-present`

* “Show me the plan”
* “Walk me through the sprint”
* “Present the approach”

### Triggers for `/stride-implement`

* “Start implementation”
* “Begin coding”
* “Proceed with the sprint”

### Triggers for `/stride-feedback`

* “Change this part”
* “Modify the plan”
* “Update the design”
* “Here’s a correction”

### Triggers for `/stride-review`

* “Review the work”
* “Validate this sprint”
* “Check if this is correct”

### Triggers for `/stride-complete`

* “Finalize the sprint”
* “Wrap this up”
* “Let’s complete this”

---

# **11. Best Practices**

### Sprints MUST be:

* Small (1–3 days)
* Independent
* Fully testable
* Fully documented

### Strides MUST be:

* Sequential
* Atomic
* Outcome-oriented
* Traceable to tasks
* Fully logged

### Files MUST remain clean:

* No unused sections
* No obsolete tasks
* No ambiguity
* No cross-file contamination

---

# **12. Advanced Commands**

## **12.1 `/stride-derive` - Sprint Discovery**

### **Goal**

Analyze project context and codebase to derive multiple actionable sprint proposals, ranked by priority and effort.

### **Agent Behaviour**

1. Verify `.stride/project.md` exists (require `/stride-init` if missing)
2. Read all 11 sections of project.md to understand constraints, goals, domain
3. Scan `.stride/sprints/` directory to identify existing sprints and avoid duplicates
4. Search codebase for opportunities:
   - TODO/FIXME/HACK comments
   - Missing tests or documentation
   - Code smells (duplication, long functions, hard-coded values)
   - Security gaps
   - Performance bottlenecks
5. Cross-reference all ideas against project constraints (Section 8)
6. Generate 5-7 sprint proposals with:
   - Sprint name (4-12 chars, unique)
   - Priority (P0/P1/P2/P3)
   - Effort (S/M/L/XL)
   - Problem statement
   - Value proposition
   - Dependencies
7. Rank proposals by priority, then by value/effort ratio
8. Present in Rich table format with color coding
9. Guide user to select one and use `/stride-plan <sprint-name>`

### **Priority Guidelines**

* **P0 (Critical)**: Blockers, critical bugs, security vulnerabilities, compliance requirements
* **P1 (High)**: Major features, high-impact improvements, significant technical debt
* **P2 (Medium)**: Minor features, moderate improvements, nice-to-haves
* **P3 (Low)**: Polish, optimizations, exploratory work

### **Effort Guidelines**

* **S (Small)**: 1-2 days, < 50 lines, single file, clear scope
* **M (Medium)**: 3-5 days, < 200 lines, 2-5 files, well-defined
* **L (Large)**: 1-2 weeks, < 500 lines, multiple modules, some complexity
* **XL (Extra Large)**: 2+ weeks, > 500 lines, architectural changes, high complexity

### **Output Format**

Present sprint proposals in a Rich table:

```
╭─────────────────────── Sprint Proposals ───────────────────────╮
│ # │ Name        │ Pri │ Effort │ Problem           │ Value     │
│───┼─────────────┼─────┼────────┼───────────────────┼───────────│
│ 1 │ auth-jwt    │ P0  │ M      │ No authentication │ Security  │
│ 2 │ error-log   │ P1  │ S      │ Silent failures   │ Debug     │
│ ...                                                             │
╰─────────────────────────────────────────────────────────────────╯
```

### **Rules**

* MUST be read-only (no file creation)
* MUST check for `.stride/project.md` first
* MUST scan existing sprints to avoid duplicates
* MUST validate all proposals against project constraints
* MUST present 5-7 proposals minimum
* MUST rank by priority and value/effort
* MUST guide user to `/stride-plan` after selection
* Output MUST use Rich table formatting

---

## **12.2 `/stride-lite` - Lightweight Workflow**

### **Goal**

Execute small changes following Five-Stage Workflow entirely in chat without creating sprint files.

### **Lite-Eligibility Criteria**

Change must meet ALL criteria:

* **Lines Changed**: < 50 lines total
* **Files Affected**: < 3 files
* **Single Concern**: One specific fix/change only
* **No Architecture**: No design decisions or API changes
* **No Security Impact**: No auth or sensitive data
* **No New Features**: Bug fixes, styling, docs, configs only

If ANY criterion fails → abort and suggest `/stride-plan`.

### **Five-Stage Process (Chat-Based)**

#### **Stage 1: TALK (Discovery)**
- Ask clarifying questions
- Estimate scope (lines, files, complexity)
- Validate lite-eligibility against all 6 criteria
- If eligible → proceed
- If not → abort and suggest `/stride-plan`

#### **Stage 2: PLAN (Design)**
- List all files to be modified
- Describe specific changes (with line numbers if known)
- Explain reasoning and impact
- Show before/after snippets (optional)
- Ask: "Proceed with this plan?"

#### **Stage 3: CONFIRM (Approval)**
- Wait for explicit "Proceed" or "Yes"
- If user requests changes → update plan and recheck eligibility
- If scope expands beyond limits → abort
- Never skip this stage

#### **Stage 4: IMPLEMENT (Execution)**
- Make approved changes
- Monitor scope (abort if exceeds 50 lines)
- Explain each modification in chat
- Show diffs or summaries (not full file dumps)
- Confirm changes applied

#### **Stage 5: COMPLETE (Verification)**
- Provide final summary
- List all changes (files, line counts)
- Confirm quality checks
- Offer follow-up assistance
- No files created (chat-only)

### **Abort Conditions**

Stop and suggest `/stride-plan` if:
- Scope exceeds 50 lines or 3 files
- Architecture decisions needed
- Security concerns emerge
- Multiple concerns discovered
- Complexity grows beyond lite scope

### **Rules**

* MUST validate eligibility in TALK stage
* MUST follow all 5 stages (no skipping)
* MUST get explicit approval in CONFIRM stage
* MUST abort if scope exceeds limits
* MUST NOT create any files or directories
* MUST NOT log to implementation.md
* MUST NOT update project.md
* ALL communication in chat only

---

## **12.3 `/stride-status` - Conversational Status**

### **Goal**

Provide deep, conversational project status with progress analysis, blocker identification, and actionable recommendations.

### **Agent Behaviour**

1. Validate `.stride/project.md` exists (require `/stride-init` if missing)
2. Scan `.stride/sprints/` directory for all sprint folders
3. For each sprint:
   - Determine lifecycle phase (file existence)
   - If ACTIVE:
     - Parse `plan.md`: count total Strides in "## Strides" section
     - Parse `implementation.md`: count completed Stride logs (pattern: `## [Timestamp] Stride:`)
     - Calculate: `completion_pct = (completed / total) × 100`
     - Extract current Stride from latest log
     - Scan for blocker keywords: "blocker", "blocked", "cannot proceed", "waiting for"
     - Check staleness: `days_since_update > 7`
4. Calculate project health:
   - **Blocked**: any sprint has active blockers
   - **At Risk**: > 2 stale sprints OR no active work with many proposed
   - **Healthy**: normal operation
5. Generate recommendations:
   - Blocked sprints → suggest resolution
   - High completion (> 90%) → suggest `/stride-review`
   - Stale sprints → suggest `/stride-feedback` or `/stride-complete`
   - No active work → suggest starting proposed sprints
6. Format as conversational prose with emojis
7. Present naturally with encouragement

### **Progress Calculation**

**Total Strides** (from `plan.md`):
```
Find section: ## Strides (Sub-Tasks)
Count numbered items: 1. **Stride 1:**, 2. **Stride 2:**, etc.
```

**Completed Strides** (from `implementation.md`):
```
Find all logs: ## [Timestamp] Stride: [Name]
Extract unique Stride names
Count unique Strides
```

**Percentage**:
```
completion = (completed_strides / total_strides) × 100
```

### **Blocker Detection**

Search `implementation.md` for keywords:
- "blocker", "blocked"
- "cannot proceed", "waiting for"
- "needs clarification", "dependency missing"

Extract context around keyword for description.

### **Health Assessment**

```
IF any sprint has blockers → Blocked 🚫
ELSE IF stale_count > 2 → At Risk ⚠️
ELSE IF active == 0 AND proposed > 5 → At Risk ⚠️
ELSE → Healthy ✅
```

### **Output Format**

Conversational prose with structure:

```
Project Health: {status} {emoji}

Active Sprints ({count}):
{sprint_id} is {pct}% complete
- Currently on Stride {n} of {total}: "{name}"
- {blocker_status}
- Next: {action}

Proposed Sprints ({count}): {names}

Completed Recently:
- {sprint} ({days} days ago)

Recommendations:
1. {action_1}
2. {action_2}
```

### **Rules**

* MUST be read-only (no file modifications)
* MUST parse logs for accurate progress
* MUST identify all blockers from keywords
* MUST calculate completion percentages
* MUST generate specific recommendations
* Output MUST be conversational prose (not tables)
* MUST use emojis: ✅ ⚠️ 🚫
* MUST be encouraging and constructive

---

# **Final Notes (Authoritative)**

* `.stride/project.md` = **global project contract**
* `proposal.md` = **intent**
* `plan.md` = **contract & Stride definition**
* `design.md` = **technical blueprint**
* `implementation.md` = **execution log (append-only)**
* `retrospective.md` = **learning archive**

Stride is a **file-driven, spec-enforced, agent-governed engineering system.**
Agents MUST follow these rules precisely to ensure consistent, auditable, high-quality development.