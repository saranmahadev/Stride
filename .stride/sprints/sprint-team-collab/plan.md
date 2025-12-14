# Plan

## Overview

This sprint implements Git-based team collaboration features for Stride, targeting small teams (2-10 developers). The implementation follows a 7-stride sequential approach that builds team management infrastructure, then layered assignment, approval, and communication features on top.

**Strategy:** Start with foundational data models and CLI infrastructure (Strides 1-2), implement core team management (Stride 3), add assignment logic (Stride 4), build approval workflows (Stride 5), implement comment system (Stride 6), and finish with AI-powered enhancements (Stride 7).

**Key Concerns:**
- Maintain backward compatibility with v1.0 solo workflows
- Ensure atomic Git operations to prevent file corruption
- Keep performance under 2-second threshold for all commands
- Preserve offline-first, zero-infrastructure philosophy
- Design schemas that scale to v1.8 cloud features without breaking changes

The work directly implements ROADMAP.md Phase 2 (v1.5) requirements and aligns with `.stride/project.md` Section 5 architecture (file-based state management) and Section 6 conventions (CLI-native, Python 3.8+).

---

## Strides

### **Stride 1: Data Models & Schema Design**

**Purpose:**  
Establish Pydantic models and YAML schemas for team configuration, sprint metadata, and comments. This provides type-safe validation and serialization for all team-related data structures.

**Tasks:**  
- [ ] Task 1.1: Define `TeamConfig` Pydantic model with fields: project_name, members (list), roles (dict), approval_policy (dict)
- [ ] Task 1.2: Define `TeamMember` Pydantic model with fields: username, email, role, joined_at, active (bool)
- [ ] Task 1.3: Define `SprintMetadata` Pydantic model with fields: sprint_id, assignee, created_at, assigned_at, status, approvals (list), tags (list)
- [ ] Task 1.4: Define `Comment` Pydantic model with fields: id, author, timestamp, message, file_path, line_number, status, replies (list)
- [ ] Task 1.5: Create YAML schema templates for `.stride/team.yaml` structure
- [ ] Task 1.6: Create YAML schema templates for `.stride/sprints/<ID>/.metadata.yaml` structure
- [ ] Task 1.7: Create YAML schema templates for `.stride/sprints/<ID>/.comments.yaml` structure
- [ ] Task 1.8: Add models to `stride/models.py` with comprehensive docstrings
- [ ] Task 1.9: Write unit tests for model validation (valid/invalid data)
- [ ] Task 1.10: Document schema versioning strategy for future compatibility

**Completion Definition:**  
- All Pydantic models defined with proper types and validators
- YAML schemas validated against example data
- Unit tests pass with >90% coverage for models
- Models align with `.stride/project.md` Section 7 domain entities

---

### **Stride 2: File Management Infrastructure**

**Purpose:**  
Build reusable file I/O utilities for reading/writing team.yaml, metadata.yaml, and comments.yaml with atomic operations and error handling.

**Tasks:**  
- [ ] Task 2.1: Create `stride/core/team_file_manager.py` module
- [ ] Task 2.2: Implement `read_team_config()` function with validation and error handling
- [ ] Task 2.3: Implement `write_team_config()` function with atomic file operations
- [ ] Task 2.4: Implement `read_sprint_metadata()` function for metadata.yaml parsing
- [ ] Task 2.5: Implement `write_sprint_metadata()` function with version preservation
- [ ] Task 2.6: Implement `read_comments()` function for comments.yaml parsing
- [ ] Task 2.7: Implement `append_comment()` function with thread safety
- [ ] Task 2.8: Add validation checks for file existence and permissions
- [ ] Task 2.9: Implement rollback mechanism for failed write operations
- [ ] Task 2.10: Write integration tests for file operations with Git staging
- [ ] Task 2.11: Add logging for all file operations (debug level)

**Completion Definition:**  
- All file I/O functions handle edge cases (missing files, corrupt YAML, permissions)
- Atomic operations prevent partial writes
- Integration tests verify Git compatibility
- Error messages provide actionable remediation steps

---

### **Stride 3: Team Management CLI Commands**

**Purpose:**  
Implement `stride team init`, `stride team add`, `stride team remove`, `stride team list`, and `stride team edit` commands with Rich formatting and AI-assisted features.

**Tasks:**  
- [ ] Task 3.1: Create `stride/commands/team.py` module with Typer app
- [ ] Task 3.2: Implement `stride team init` command to generate `.stride/team.yaml`
- [ ] Task 3.3: Add AI role suggestion logic based on `project.md` analysis (optional prompt)
- [ ] Task 3.4: Implement `stride team add <username> --role <role> --email <email>` command
- [ ] Task 3.5: Implement `stride team remove <username>` with active sprint validation
- [ ] Task 3.6: Implement `stride team list` with Rich table formatting (columns: username, email, role, joined, active)
- [ ] Task 3.7: Implement `stride team edit <username> --role <role>` command
- [ ] Task 3.8: Add role validation against predefined roles (admin, developer, reviewer, viewer)
- [ ] Task 3.9: Implement `stride team show <username>` for member details
- [ ] Task 3.10: Add comprehensive help text and examples for all team commands
- [ ] Task 3.11: Write CLI tests using Typer's CliRunner
- [ ] Task 3.12: Update `stride/cli.py` to register team command group

**Completion Definition:**  
- All team commands execute successfully and create/modify `.stride/team.yaml`
- AI role suggestions analyze project.md technical stack and recommend roles
- Rich formatting matches existing Stride CLI styling
- Help text provides clear examples and parameter descriptions
- Team member removal blocked if member has active sprint assignments

---

### **Stride 4: Sprint Assignment System**

**Purpose:**  
Build sprint assignment logic with `stride assign` and `stride unassign` commands, metadata tracking, and AI-powered assignee recommendations.

**Tasks:**  
- [ ] Task 4.1: Create `stride/core/assignment_manager.py` module
- [ ] Task 4.2: Implement `assign_sprint()` function to create/update `.metadata.yaml`
- [ ] Task 4.3: Implement `unassign_sprint()` function with history preservation
- [ ] Task 4.4: Implement `get_assigned_sprints(username)` query function
- [ ] Task 4.5: Create `stride/commands/assign.py` with `stride assign <sprint-id> --to <username>` command
- [ ] Task 4.6: Add AI assignee suggestion logic analyzing workload and sprint complexity
- [ ] Task 4.7: Implement interactive prompt when `--to` not specified (show recommendations)
- [ ] Task 4.8: Validate assignee exists in `team.yaml` before assignment
- [ ] Task 4.9: Enhance `stride list` to display assignee column
- [ ] Task 4.10: Enhance `stride show <sprint-id>` to display assignment metadata
- [ ] Task 4.11: Add `stride list --assignee <username>` filter flag
- [ ] Task 4.12: Write tests for assignment edge cases (invalid user, reassignment, unassignment)

**Completion Definition:**  
- Sprint assignment creates valid `.metadata.yaml` in sprint directory
- AI recommendations consider current member workload (active sprint count)
- Assignment metadata persists across Git commits
- CLI displays assignment info in list and show commands
- Validation prevents assigning to non-existent team members

---

### **Stride 5: Approval Workflow System**

**Purpose:**  
Implement approval workflow with configurable N-required-reviewers policy, `stride approve` command, and sprint completion validation.

**Tasks:**  
- [ ] Task 5.1: Add `approval_policy` section to team.yaml schema (required_approvers, allow_self_approval)
- [ ] Task 5.2: Create `stride/core/approval_manager.py` module
- [ ] Task 5.3: Implement `approve_sprint(sprint_id, approver)` function
- [ ] Task 5.4: Implement `get_approval_status(sprint_id)` returning (approved_count, required_count, approvers)
- [ ] Task 5.5: Implement `can_approve(sprint_id, username)` validation (not assignee if self-approval disabled)
- [ ] Task 5.6: Create `stride approve <sprint-id>` command
- [ ] Task 5.7: Add approval status display to `stride show <sprint-id>` (progress bar: 2/3 approvals)
- [ ] Task 5.8: Enhance `stride complete` to validate approval threshold before completion
- [ ] Task 5.9: Add approval count badge to `stride list` output
- [ ] Task 5.10: Implement `stride unapprove <sprint-id>` command for approval retraction
- [ ] Task 5.11: Write tests for approval edge cases (duplicate approval, self-approval, threshold validation)

**Completion Definition:**  
- Approval policy configured in team.yaml and enforced at runtime
- `stride complete` blocked with clear error if approvals insufficient
- Approval status visible in CLI with Rich progress bar
- Approval history preserved in metadata.yaml with timestamps
- Self-approval blocked when policy disallows it

---

### **Stride 6: Comment & Communication System**

**Purpose:**  
Build threaded comment system with file/line anchoring, stored in `.comments.yaml`, accessible via `stride comment` commands.

**Tasks:**  
- [ ] Task 6.1: Create `stride/core/comment_manager.py` module
- [ ] Task 6.2: Implement `add_comment(sprint_id, author, message, file_path, line)` function
- [ ] Task 6.3: Implement `get_comments(sprint_id, filter)` function supporting filtering (open/resolved/all)
- [ ] Task 6.4: Implement `resolve_comment(comment_id)` function
- [ ] Task 6.5: Implement `reply_to_comment(comment_id, author, message)` for threading
- [ ] Task 6.6: Create `stride comment <sprint-id> "message"` command with optional `--file` and `--line` flags
- [ ] Task 6.7: Create `stride comments <sprint-id>` command to display all comments in threaded view
- [ ] Task 6.8: Implement Rich formatting for comments (indented replies, color-coded status)
- [ ] Task 6.9: Create `stride comment resolve <comment-id>` command
- [ ] Task 6.10: Add comment count to `stride show <sprint-id>` header
- [ ] Task 6.11: Implement comment ID generation (unique per sprint)
- [ ] Task 6.12: Write tests for comment threading and resolution logic

**Completion Definition:**  
- Comments stored in `.comments.yaml` with valid schema
- Threaded replies displayed with proper indentation
- File/line anchoring optional but preserved when provided
- Comment resolution changes status without deleting content
- Comments version-controlled and visible in Git history

---

### **Stride 7: Workload Balancing**

**Purpose:**  
Implement workload tracking and balancing features to help teams distribute sprint assignments evenly across members.

**Tasks:**  
- [ ] Task 7.1: Create `stride/core/workload_analyzer.py` module
- [ ] Task 7.2: Implement `calculate_member_workload()` analyzing active/pending sprint counts per member
- [ ] Task 7.3: Implement sprint complexity scoring based on stride count and task count
- [ ] Task 7.4: Implement workload balancing algorithm to identify overloaded/underutilized members
- [ ] Task 7.5: Enhance `stride assign workload` command to show detailed per-member breakdown
- [ ] Task 7.6: Add workload score calculation (weighted by sprint complexity)
- [ ] Task 7.7: Implement workload visualization with Rich progress bars per member
- [ ] Task 7.8: Add workload metrics to `stride metrics` command output (average, min, max, std deviation)
- [ ] Task 7.9: Implement `--export json` flag for programmatic workload access
- [ ] Task 7.10: Write tests for workload calculation accuracy with edge cases
- [ ] Task 7.11: Document workload scoring algorithm in code comments

**Completion Definition:**  
- `stride assign workload` displays accurate per-member sprint counts with complexity scores
- Workload metrics show distribution across team (min/max/avg/std dev)
- Sprint complexity scoring considers stride count, task count as factors
- Workload visualization uses Rich progress bars for visual comparison
- Export flag provides JSON output for external analysis

---

## Approach

**Technical Strategy:**

This sprint follows Stride's established patterns from v1.0:
- **File-based state management**: All team data stored in YAML files within `.stride/`
- **CLI-native interface**: Rich-formatted terminal commands using Typer framework
- **Pydantic validation**: Type-safe models ensure data integrity
- **Atomic operations**: File writes use temp files + rename for atomicity
- **Git-friendly**: YAML formats designed for meaningful diffs

**Architecture Alignment:**
- Extends existing `stride/core/` modules with team-specific managers
- Follows `stride/commands/` pattern for new CLI command groups
- Reuses `stride/models.py` for data validation
- Leverages existing `stride/utils.py` for formatting and helpers

**Sequencing Rationale:**
1. **Strides 1-2 (Foundation)**: Data models and file I/O must be solid before building features
2. **Stride 3 (Team Management)**: Team membership required before assignments
3. **Stride 4 (Assignments)**: Ownership needed before approval workflows
4. **Stride 5 (Approvals)**: Approval system depends on assignment metadata
5. **Stride 6 (Comments)**: Communication layer builds on established team structure
6. **Stride 7 (Workload)**: Analytics require all data models and assignments populated

**Testing Strategy:**
- **Unit tests**: Pydantic model validation, individual function logic
- **Integration tests**: File I/O with actual YAML files, Git staging verification
- **CLI tests**: Typer CliRunner for command execution and output validation
- **Manual tests**: End-to-end team workflows (init → add → assign → approve → complete)

**Code Structure:**
```
stride/
├── models.py                      # Add TeamConfig, TeamMember, SprintMetadata, Comment
├── commands/
│   ├── team.py                    # New: team management commands
│   ├── assign.py                  # New: assignment commands
│   └── workload.py                # New: workload command
├── core/
│   ├── team_file_manager.py      # New: YAML I/O for team files
│   ├── assignment_manager.py     # New: assignment logic
│   ├── approval_manager.py       # New: approval workflow
│   ├── comment_manager.py        # New: comment system
│   └── workload_analyzer.py      # New: workload calculations
└── utils.py                       # Enhance with team formatting helpers
```

**Risk Containment:**
- Schema versioning strategy allows future migrations
- Backward compatibility ensured by making all team features opt-in
- File corruption prevented via atomic writes and validation
- Performance tested with simulated 50-member teams

**Alignment with `.stride/project.md`:**
- Section 5 (Architecture): Maintains modular monolith pattern
- Section 6.1 (Coding): Follows snake_case, Black formatting, docstring requirements
- Section 6.3 (Testing): Meets 80% coverage target for new code
- Section 8.1 (Constraints): Python 3.8+ compatibility preserved

---

## Dependencies

**Technical Dependencies (All Satisfied):**
- PyYAML >= 6.0.0 (already in project dependencies)
- Rich >= 13.0.0 (already in project dependencies)
- Pydantic >= 2.0.0 (already in project dependencies)
- Typer >= 0.9.0 (already in project dependencies)

**Architectural Dependencies (All Satisfied):**
- `.stride/project.md` exists (enforced by init workflow)
- Sprint structure from v1.0 unchanged (backward compatibility requirement)
- File-based state management pattern (existing architecture)

**Development Dependencies:**
- pytest for unit/integration testing (already in dev dependencies)
- black for code formatting (already in dev dependencies)
- mypy for type checking (already in dev dependencies)

**External Dependencies:**
None. This sprint requires zero external services, APIs, or infrastructure.

**Blocker Status:**
No blockers identified. All dependencies are internal and under development team control.

---

## Risks

### Risk: Schema Evolution Complexity

**Impact:** Medium

Schema changes in future versions could break existing team.yaml or metadata.yaml files, requiring migration logic.

**Mitigation:**
- Add schema version field to all YAML files (`schema_version: "1.5"`)
- Document migration strategy in code comments
- Design schemas with extensibility in mind (allow extra fields)
- Write validation that provides clear upgrade guidance

---

### Risk: Git Merge Conflicts in Team Files

**Impact:** Medium

Multiple developers simultaneously editing team.yaml or metadata.yaml could cause merge conflicts.

**Mitigation:**
- Design YAML structure to minimize conflict potential (list-based members, not nested objects)
- Document merge resolution strategies in user guide
- Consider future conflict resolution tools in v1.8
- For now, document best practice: pull before team operations

---

### Risk: Performance Degradation with Large Teams

**Impact:** Low (for v1.5 target of 2-10 members)

Workload calculations and member lookups could slow down with 50+ members.

**Mitigation:**
- Benchmark with simulated 50-member teams
- Add caching for workload calculations
- Defer optimization to v2.0 if 2-10 member performance acceptable
- Document team size limits in README

---

### Risk: AI Suggestion Quality

**Impact:** Low

AI-powered role suggestions and assignee recommendations may be inaccurate or unhelpful.

**Mitigation:**
- Make AI suggestions optional (users can ignore)
- Provide manual override for all automated suggestions
- Log suggestion reasoning for debugging
- Iterate based on user feedback in v1.6

---

### Risk: Backward Compatibility Break

**Impact:** High (would violate roadmap commitment)

New team features could interfere with v1.0 solo developer workflows.

**Mitigation:**
- Team features strictly opt-in (require `stride team init`)
- All existing commands work without team.yaml present
- Test suite includes v1.0 compatibility regression tests
- Document upgrade path in CHANGELOG.md

---

## Validation Plan

### Functional Validation

**Team Management:**
- [ ] Create team with `stride team init` and verify team.yaml structure
- [ ] Add 5 members with different roles and verify uniqueness enforcement
- [ ] Remove member without active sprints successfully
- [ ] Attempt to remove member with active sprint and verify block
- [ ] List team members and verify formatting and data accuracy

**Sprint Assignment:**
- [ ] Assign sprint to team member and verify metadata.yaml creation
- [ ] Reassign sprint and verify history preservation
- [ ] Filter sprints by assignee and verify accuracy
- [ ] Verify AI assignee suggestions based on workload
- [ ] Unassign sprint and verify metadata update

**Approval Workflow:**
- [ ] Configure 2-required-approvers policy in team.yaml
- [ ] Two team members approve sprint successfully
- [ ] Attempt sprint completion with 1/2 approvals and verify block
- [ ] Complete sprint with 2/2 approvals successfully
- [ ] Verify self-approval blocked when policy disallows

**Comments:**
- [ ] Add top-level comment to sprint
- [ ] Add file-anchored comment with file path and line number
- [ ] Reply to comment and verify threading
- [ ] Resolve comment and verify status change
- [ ] View all comments and verify Rich formatting

**Workload Balancing:**
- [ ] Run `stride workload` and verify member sprint counts
- [ ] Assign sprints to balance load and verify score changes
- [ ] Verify AI recommendations prioritize low-workload members

---

### Technical Validation

**Architecture Alignment:**
- [ ] All new modules follow `.stride/project.md` Section 5 architecture pattern
- [ ] File I/O uses atomic operations (temp file + rename)
- [ ] Pydantic models validate all YAML data
- [ ] Git diffs for YAML files are human-readable

**Code Quality:**
- [ ] Black formatting passes (100 char lines)
- [ ] isort import ordering passes
- [ ] mypy type checking passes with no errors
- [ ] No hardcoded secrets or credentials
- [ ] All functions have docstrings with Args/Returns/Raises

**Error Handling:**
- [ ] Invalid team operations display actionable error messages
- [ ] Missing team.yaml handled gracefully (prompt to run `stride team init`)
- [ ] Corrupt YAML files provide parse error with line number
- [ ] Permission errors display clear remediation steps

**Performance:**
- [ ] All team commands complete within 2-second threshold
- [ ] Workload calculations handle 50 members without degradation
- [ ] File I/O operations do not block unnecessarily

---

### Quality Gates

**Linting:**
- [ ] `black stride/` reports no formatting issues
- [ ] `isort stride/` reports no import ordering issues
- [ ] No unused imports or variables

**Security:**
- [ ] No hardcoded credentials in team.yaml or metadata.yaml
- [ ] File permissions set appropriately (644 for YAML files)
- [ ] No SQL injection vulnerabilities (N/A - no SQL)
- [ ] No path traversal vulnerabilities in file operations

**Test Coverage:**
- [ ] Overall coverage >80% for new code
- [ ] Core modules (team_manager, assignment_manager, approval_manager) >90% coverage
- [ ] All edge cases covered (invalid data, missing files, corrupt YAML)

**Documentation:**
- [ ] README.md updated with team collaboration section
- [ ] FEATURES.md updated with v1.5 team features
- [ ] CHANGELOG.md entry added for v1.5
- [ ] Help text comprehensive for all new commands
- [ ] Example workflows documented

---

## Completion Conditions

A sprint is complete when:

1. **All Strides Marked Complete**
   - All 7 strides completed with all tasks checked

2. **All Acceptance Criteria Met**
   - 40+ acceptance criteria from proposal.md validated

3. **Code Quality Gates Passed**
   - Black, isort, mypy pass without errors
   - Test coverage >80% overall, >90% for core modules
   - No security vulnerabilities detected

4. **Documentation Updated**
   - README.md, FEATURES.md, CHANGELOG.md updated
   - Help text written for all new commands
   - User workflows documented with examples

5. **Manual Testing Complete**
   - End-to-end team workflows tested (init → assign → approve → complete)
   - Edge cases manually verified (conflicts, invalid data, missing files)
   - Backward compatibility with v1.0 confirmed

6. **Implementation Logs Accurate**
   - `implementation.md` reflects each stride accurately
   - All decisions and trade-offs documented

7. **Validation Passes**
   - `stride validate sprint-team-collab` passes without warnings
   - All quality gates satisfied

8. **ROADMAP.md Phase 2 Goals Achieved**
   - Team initialization ✓
   - Member management ✓
   - Assignment & workflow ✓
   - Comments & communication ✓

---
