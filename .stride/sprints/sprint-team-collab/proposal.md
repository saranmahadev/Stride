# Proposal: Repo-Based Team Collaboration

## Why

**Problem Statement:**
Stride v1.0 is designed exclusively for solo developers working with AI agents. Small teams (2-10 developers) have no native way to collaborate on sprints, assign work, track ownership, or communicate within the Stride workflow. Teams are forced to use external tools (Jira, Slack, email) which breaks the repo-first, CLI-native philosophy and creates context fragmentation.

**Negative Impact of Not Solving:**
- Teams cannot adopt Stride without external project management tools
- Sprint ownership and accountability are unclear in multi-developer scenarios
- No mechanism for peer review or approval workflows
- Team coordination happens outside the repository, losing Git's versioning benefits
- Stride's value proposition (unified, repo-native workflow) fails for teams

**Positive Impact Expected:**
- Small teams can collaborate entirely through Git with no external dependencies
- Sprint assignments, ownership, and approvals stored in `.stride/` (version-controlled)
- Built-in commenting system enables threaded discussions on sprint files
- AI-assisted member management and workload balancing
- Maintains privacy-first, offline-capable design
- Positions Stride for v1.8 cloud-optional features without architectural rewrites

**Business Value:**
- Expands target market from solo developers to small teams (2-10 members)
- Differentiates from competitors by offering zero-infrastructure team collaboration
- Aligns with ROADMAP.md Phase 2 goals for Q1-Q2 2025
- Creates foundation for enterprise features in v2.0

---

## What

This sprint implements Git-based team collaboration features enabling small teams to work on Stride sprints together without external infrastructure.

### In Scope

**Team Management:**
- `stride team init` command to generate `.stride/team.yaml`
- Team configuration schema: members, roles, policies
- `stride team add <username> --role <role>` command
- `stride team remove <username>` command
- `stride team edit <username> --role <role>` command
- `stride team list` command with role-based filtering
- AI-assisted role suggestions based on `project.md` analysis

**Sprint Assignment:**
- `stride assign <sprint-id> --to <username>` command
- Sprint metadata tracking in `.stride/sprints/<ID>/.metadata.yaml`
- Ownership, assignee, approvers fields
- `stride unassign <sprint-id>` command
- AI-suggested assignees based on workload and expertise

**Approval Workflow:**
- Configurable N-required-reviewers policy in `team.yaml`
- `stride approve <sprint-id>` command
- Approval tracking in sprint metadata
- Block sprint completion until approval threshold met
- Visual approval status in `stride status` and `stride show`

**Comments & Communication:**
- Threaded comment system stored in `.stride/sprints/<ID>/.comments.yaml`
- `stride comment <sprint-id> "message"` command
- File and line-level comment anchoring
- `stride comments <sprint-id>` to view all comments
- Comment resolution workflow (open/resolved status)

**Workload Balancing:**
- `stride workload` command showing per-member sprint assignments
- AI-assisted load balancing recommendations
- Workload visualization in terminal UI

**CLI Enhancements:**
- `stride list` shows assignee information
- `stride show <sprint-id>` displays ownership, approvals, comments
- Color-coded role badges in terminal output
- Filter sprints by assignee: `stride list --assignee <username>`

### Out of Scope

- Real-time collaboration features (v1.8)
- Web-based UI or dashboard (v1.7)
- Cloud synchronization (v1.6)
- External integrations (Slack, Teams) (v1.8)
- Multi-organization support (v2.0)
- SSO or advanced RBAC (v2.0)
- Agent-to-agent collaboration (v1.6+)
- Performance optimization beyond 50 members (v2.0)

---

## Acceptance Criteria

### Team Management Criteria

- [ ] `stride team init` creates `.stride/team.yaml` with valid schema
- [ ] Team configuration includes: project name, members array, roles, policies
- [ ] `stride team add` validates unique usernames and valid roles
- [ ] `stride team remove` prevents removing members with active sprint assignments
- [ ] `stride team list` displays members with roles in formatted table
- [ ] AI role suggestions analyze `project.md` and recommend appropriate roles
- [ ] Invalid team operations display actionable error messages

### Assignment Criteria

- [ ] `stride assign` creates/updates `.stride/sprints/<ID>/.metadata.yaml`
- [ ] Metadata includes: assignee, created_at, assigned_at, status, approvals array
- [ ] `stride assign` validates assignee exists in `team.yaml`
- [ ] Reassignment updates metadata and preserves history
- [ ] `stride list --assignee <username>` filters correctly
- [ ] Unassigned sprints clearly marked in CLI output
- [ ] AI assignee suggestions consider current workload and sprint complexity

### Approval Workflow Criteria

- [ ] `team.yaml` supports `approval_policy.required_approvers: N` configuration
- [ ] `stride approve` adds authenticated user to approvals array in metadata
- [ ] Approval count displayed in `stride show <sprint-id>`
- [ ] `stride complete` blocked if approval threshold not met
- [ ] Clear error message when attempting completion without approvals
- [ ] Approvers cannot approve their own sprints (self-approval blocked)
- [ ] Approval status persists in Git history

### Comments & Communication Criteria

- [ ] `stride comment <sprint-id> "message"` appends to `.comments.yaml`
- [ ] Comments include: id, author, timestamp, message, file, line, status (open/resolved)
- [ ] `stride comments <sprint-id>` displays threaded view with Rich formatting
- [ ] Comments support file and line anchoring (optional parameters)
- [ ] Comment resolution: `stride comment resolve <comment-id>`
- [ ] Comments version-controlled and visible in Git diffs
- [ ] Comment count displayed in `stride show <sprint-id>`

### Workload Balancing Criteria

- [ ] `stride workload` calculates active sprints per team member
- [ ] Workload display shows: username, active sprints, proposed sprints, completed sprints
- [ ] AI workload balancing analyzes sprint complexity and member capacity
- [ ] Recommendations displayed when running `stride assign` without `--to` parameter
- [ ] Workload metrics exported in `stride metrics` output

### CLI Integration Criteria

- [ ] All team commands follow existing Stride CLI conventions
- [ ] Rich formatting consistent with v1.0 styling (colors, tables, progress bars)
- [ ] Help text comprehensive for all new commands
- [ ] Error handling provides actionable guidance
- [ ] Commands complete within 2-second performance budget
- [ ] Git operations are atomic to prevent corruption

---

## Success Definition

A sprint is considered **successful** when:

- All acceptance criteria are satisfied
- All Strides in `plan.md` are complete
- Unit tests pass with >80% coverage for new code
- Integration tests validate Git-based workflows
- Documentation updated (README.md, FEATURES.md, CHANGELOG.md)
- No violations of `.stride/project.md` architecture patterns
- Manual testing confirms team workflows function correctly
- `stride validate sprint-team-collab` passes without warnings
- ROADMAP.md Phase 2 goals demonstrably achieved

---

## Impact

**Affected Modules:**
- `/stride/cli.py` — New command group: `team`, `assign`, `approve`, `comment`, `workload`
- `/stride/models.py` — New Pydantic models: TeamConfig, TeamMember, SprintMetadata, Comment
- `/stride/core/team_manager.py` — New module for team operations
- `/stride/core/assignment_manager.py` — New module for assignment logic
- `/stride/core/comment_manager.py` — New module for comment system
- `/stride/core/sprint_manager.py` — Enhanced with assignment and approval checks
- `/stride/commands/` — New command files: `team.py`, `assign.py`, `workload.py`
- `/stride/utils.py` — Enhanced with team-aware formatting utilities

**Affected CLI Commands:**
- `stride list` — Display assignee and approval status
- `stride show` — Display ownership, approvals, comments
- `stride status` — Show team-wide sprint distribution
- `stride complete` — Validate approval requirements
- `stride metrics` — Include team-level analytics

**New Files Created:**
- `.stride/team.yaml` — Team configuration
- `.stride/sprints/<ID>/.metadata.yaml` — Sprint ownership and approvals
- `.stride/sprints/<ID>/.comments.yaml` — Threaded comments

**Affected Teams:**
- Core development team (implementation)
- QA team (testing team workflows)
- Documentation team (user guides)

**Affected Systems:**
- CLI command routing and parsing
- File I/O for new YAML schemas
- Git integration for version control
- AI assistant integration for suggestions

**Breaking Changes:**
None. This sprint is fully backward-compatible. Solo developers (v1.0 users) can continue using Stride without team features. Team features are opt-in via `stride team init`.

---

## Dependencies

**Technical Dependencies:**
- PyYAML for team.yaml and metadata parsing (already in dependencies)
- Rich for enhanced table formatting (already in dependencies)
- Pydantic for data validation (already in dependencies)
- Git repository present (existing requirement)

**Architectural Dependencies:**
- `.stride/project.md` must exist (enforced by existing init workflow)
- Sprint structure from v1.0 must remain unchanged (backward compatibility)
- File-based state management preserved (no database required)

**Process Dependencies:**
- ROADMAP.md Phase 2 specification finalized (complete)
- Team workflow UX validated with target users (to be done during planning)
- Schema design for team.yaml and metadata.yaml validated (to be done in design phase)

**External Dependencies:**
None. This sprint requires no external services, APIs, or infrastructure. All functionality is Git-based and offline-capable.

**Blockers:**
None identified. All dependencies are satisfied or under control of the development team.

---
