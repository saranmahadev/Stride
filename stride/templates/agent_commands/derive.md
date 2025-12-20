---
description: Analyze project context and derive multiple sprint proposals for user selection.
---

$ARGUMENTS
<!-- STRIDE:START -->

**Guardrails**
- `/stride-derive` is a **read-only** command. It must never create sprint files or directories.
- Only analyze existing project context and codebase to generate sprint ideas.
- Never begin planning or implementation during this command.
- Output must be presented as a ranked, prioritized list in a Rich table format.
- All sprint proposals must align with constraints defined in `.stride/project.md`.
- Must check for duplicate sprint ideas already in `.stride/sprints/`.
- Sprint proposals must be actionable and specific, not vague suggestions.

---

**Steps**

1. **Validate Project Context**  
   - Verify `.stride/project.md` exists.  
   - If missing, stop and instruct user to run `/stride-init` first.  
   - Read all 11 sections to understand:  
     - Project goals and scope (Section 1-2)  
     - Technical constraints (Section 4, 8.1)  
     - Domain knowledge (Section 7)  
     - Known risks (Section 11)  
   - **Learnings Check**: Read `learnings.md` to avoid repeating past mistakes or to find inspiration.

2. **Analyze Existing Sprints**  
   - Scan `.stride/sprints/` directory for existing sprint folders.  
   - Extract sprint names to avoid duplicate proposals.  
   - Identify completed vs active vs proposed sprints.  
   - Look for patterns or gaps (e.g., many feature sprints but no testing sprints).

3. **Scan Codebase for Opportunities**  
   Use grep/search to find:  
   - `TODO` comments → potential improvement tasks  
   - `FIXME` comments → bugs or technical debt  
   - `HACK` or `XXX` markers → areas needing refactoring  
   - Missing test files → testing gaps  
   - Incomplete error handling → reliability improvements  
   - Hard-coded values → configuration needs  
   - Deprecated APIs → migration opportunities  
   - Documentation gaps → docs sprints  

4. **NICE Marker Analysis**
   - Scan for NICE markers to understand system intent and coverage.
   - Identify areas with missing markers (potential technical debt).
   - Identify markers with `TODO` or `FIXME` tags.
   - Use marker relationships to find coupled components that need joint refactoring.

5. **Identify Technical Debt & Gaps**  
   - Analyze code patterns for:  
     - Duplicated logic → refactor opportunities  
     - Long functions/files → modularity improvements  
     - Missing abstractions → architecture refinements  
     - Inconsistent naming → standardization needs  
     - Security vulnerabilities → security hardening sprints  
     - Performance bottlenecks → optimization sprints  

6. **Cross-Reference with Project Constraints**  
   - Filter ideas against Section 8 (Constraints) to ensure feasibility.  
   - Ensure proposals respect Section 6 (Standards & Conventions).  
   - Verify alignment with Section 3 (Non-Functional Requirements).  

7. **Generate 5-7 Sprint Proposals**  
   For each proposal, define:  
   - **Sprint Name**: 4-12 chars, domain-relevant, unique (e.g., `auth`, `ui-polish`, `perf-opt`)  
   - **Priority**: P0 (critical), P1 (high), P2 (medium), P3 (low)  
   - **Effort**: S (1-2 days), M (3-5 days), L (1-2 weeks), XL (2+ weeks)  
   - **Problem Statement**: 1-2 sentences describing what's broken/missing  
   - **Value Proposition**: Why this matters (user impact, risk reduction, tech debt payoff)  
   - **Dependencies**: List any required sprints that must be completed first  

   **Priority Guidelines:**  
   - P0: Blockers, critical bugs, security issues, compliance requirements  
   - P1: Major features, high-impact improvements, significant debt  
   - P2: Minor features, moderate improvements, nice-to-haves  
   - P3: Polish, optimizations, exploratory work  

   **Effort Guidelines:**  
   - S: < 50 lines changed, single file, clear scope  
   - M: < 200 lines, 2-5 files, well-defined  
   - L: < 500 lines, multiple modules, some complexity  
   - XL: > 500 lines, architectural changes, high complexity  

8. **Rank Proposals**  
   Sort by:  
   1. Priority (P0 first)  
   2. Value/Effort ratio (quick wins higher)  
   3. Dependencies (independent sprints first)  

9. **Present Sprint Proposals**
   Display proposals in a clean, presentable list format (no table for the main list). Use emojis and clear headings.

   **Example Format:**
   
   🚀 **Sprint 1: Auth Refactor** (P0 - High Priority)
   - **Problem**: No authentication system currently exists.
   - **Value**: Critical for security and user management.
   - **Effort**: Medium (3-5 days)
   - **Dependencies**: None

   🛠️ **Sprint 2: Error Logging** (P1 - Medium Priority)
   - **Problem**: Silent failures make debugging impossible.
   - **Value**: Improves reliability and developer experience.
   - **Effort**: Small (1-2 days)
   - **Dependencies**: None

   ...

   **Summary Table** (at the end):
   ```
   | # | Name        | Pri | Effort | Value     |
   |---|-------------|-----|--------|-----------|
   | 1 | auth-jwt    | P0  | M      | Security  |
   | 2 | error-log   | P1  | S      | Debug     |
   ...
   ```

10. **Provide Selection Guidance**
   - Highlight P0/P1 items as recommended starting points.  
   - Suggest quick wins (P1/S or P2/S) for momentum.  
   - Note any blocking dependencies.  
   - Ask user: **"Which sprint would you like to plan? (Enter number or name)"**  

11. **Guide to Next Step**  
    After user selects a sprint (e.g., #3 or "auth"):  
    - Confirm selection  
    - Instruct: **"Run `/stride-plan sprint-[NAME]` to create this sprint."**  
    - Do NOT automatically create the sprint folder or files.  

---

**When to Trigger**  
The command MUST trigger when the user says:  
- "Derive sprint ideas"  
- "What should we work on next?"  
- "Show me potential sprints"  
- "Suggest sprint backlog"  
- "What needs to be done?"  
- "Help me prioritize work"  
- "Analyze the codebase for tasks"  

---

**When NOT to Trigger**
- When `.stride/project.md` doesn't exist (require `/stride-init` first)  
- When user already knows the sprint they want (use `/stride-plan` directly)  
- During active sprint implementation (`/stride-implement`)  
- When asking for project status (use `/stride-status`)  
- When making mid-sprint adjustments (use `/stride-feedback`)  

---

**Output Example**

```
╭─────────────────────── Sprint Proposals ───────────────────────╮
│                                                                 │
│ Analyzed: 3 existing sprints | Found: 12 TODOs, 5 FIXMEs       │
│                                                                 │
│ # │ Name        │ Pri │ Effort │ Problem           │ Value     │
│───┼─────────────┼─────┼────────┼───────────────────┼───────────│
│ 1 │ auth-jwt    │ P0  │ M      │ No authentication │ Security  │
│ 2 │ error-log   │ P1  │ S      │ Silent failures   │ Debug     │
│ 3 │ api-tests   │ P1  │ M      │ No API coverage   │ Quality   │
│ 4 │ ui-polish   │ P2  │ S      │ Inconsistent UI   │ UX        │
│ 5 │ perf-cache  │ P2  │ L      │ Slow DB queries   │ Speed     │
│ 6 │ docs-api    │ P3  │ S      │ Missing API docs  │ DevEx     │
│ 7 │ refactor-db │ P3  │ XL     │ Tech debt in ORM  │ Maintain  │
│                                                                 │
│ 🎯 Recommended: Start with #1 (P0) or #2 (quick win)          │
│                                                                 │
╰─────────────────────────────────────────────────────────────────╯

Which sprint would you like to plan? (Enter number or name)
```

---

**Rules**
- MUST NOT create any files or directories  
- MUST NOT start planning or implementation  
- MUST check `.stride/project.md` exists  
- MUST scan `.stride/sprints/` to avoid duplicates  
- MUST present at least 5 proposals (up to 7 max)  
- MUST include priority, effort, problem, value for each  
- MUST rank by priority and value/effort ratio  
- MUST use Rich table formatting for output  
- MUST guide user to `/stride-plan` after selection  
- MUST validate all proposals against project constraints  

---

**Reference**
- `.stride/project.md` — authoritative project context and constraints  
- `.stride/sprints/` — existing sprint folders to avoid duplicates  
- Codebase (TODO, FIXME, code patterns) — sources for sprint ideas  
- Stride Instructions — for sprint naming conventions and structure  

<!-- STRIDE:END -->
