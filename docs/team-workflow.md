# Team Collaboration Workflow Guide

**Stride v1.5** brings Git-based team collaboration to enable small teams (2-10 developers) to work together without external infrastructure. This guide covers everything from initial setup to advanced workflows.

## Philosophy: Repo-First, Zero-Infrastructure

Stride's team collaboration model is fundamentally different from traditional project management tools:

- **No Servers**: Collaboration happens entirely through Git push/pull
- **No Databases**: All state stored in YAML files, version-controlled by Git
- **No Cloud Dependency**: Works 100% offline (cloud sync optional in v1.6+)
- **Privacy-First**: All team data stays in your repository
- **Graceful Scaling**: Start solo, add team members later—no migration needed

**The Result**: Small teams can collaborate with the same simplicity that made Stride successful for solo developers, while maintaining complete control over their data.

---

## Getting Started

### Prerequisites

- Stride v1.5+ installed (`pip install stridekit`)
- Project initialized with `stride init`
- Git repository configured
- Team members with Git access to repository

### Quick Start (5 Minutes)

```bash
# 1. Initialize team configuration (one-time setup)
stride team init

# 2. Add team members
stride team add "Alice Johnson" alice@example.com --roles lead,reviewer
stride team add "Bob Smith" bob@example.com --roles developer

# 3. Configure approval policy
# → Set during stride team init
# → Example: 2 required approvals from lead or reviewer roles

# 4. Commit and push team configuration
git add .stride/team.yaml
git commit -m "Configure Stride team collaboration"
git push

# 5. Team members pull repository to sync
# → They can now be assigned sprints and give approvals
```

---

## Team Setup

### Initializing Team Configuration

The `stride team init` command creates `.stride/team.yaml` with your team structure:

```bash
$ stride team init

Enter project name: AwesomeApp

Add Team Members (Press Enter with empty name to finish)

Member name: Alice Johnson
Email: alice@example.com
Roles (comma-separated) [developer]: lead,reviewer
✓ Added Alice Johnson

Member name: Bob Smith
Email: bob@example.com
Roles (comma-separated) [developer]: developer
✓ Added Bob Smith

Member name: Carol Lee
Email: carol@example.com
Roles (comma-separated) [developer]: developer,reviewer
✓ Added Carol Lee

Member name: [Press Enter]

Approval Policy
Enable approval workflow? [y/n]: y
Required approvals: 2
Roles that can approve (comma-separated) [lead,reviewer]: lead,reviewer

✓ Team configuration created!
File: .stride/team.yaml
3 team members configured
Approval workflow: enabled (2 required)
```

**What gets created:**

```yaml
# .stride/team.yaml
project_name: AwesomeApp
members:
  - email: alice@example.com
    name: Alice Johnson
    roles:
      lead: true
      reviewer: true
    joined_at: "2025-12-14T10:30:00Z"
    active: true
  - email: bob@example.com
    name: Bob Smith
    roles:
      developer: true
    joined_at: "2025-12-14T10:31:00Z"
    active: true
  # ... more members
approval_policy:
  enabled: true
  required_approvals: 2
  roles_can_approve:
    - lead
    - reviewer
```

### Available Roles

- **lead**: Team lead with full permissions (can assign, approve, manage team)
- **developer**: Can be assigned sprints and implement features
- **reviewer**: Can approve sprints (typically paired with lead or developer)
- **designer**: Design-focused role
- **qa**: Quality assurance specialist
- **docs**: Documentation specialist

Roles are flexible—assign multiple roles per member as needed.

### Managing Team Members

**Add member:**
```bash
stride team add "David Chen" david@example.com --roles developer,qa
```

**Update member:**
```bash
stride team edit alice@example.com --roles lead,developer,reviewer
```

**Remove member:**
```bash
stride team remove david@example.com
```

**Safeguard**: Removal blocked if member has active sprint assignments.

**View member details:**
```bash
stride team show alice@example.com
```

**List all members:**
```bash
stride team list
```

---

## Sprint Assignment

### Interactive Assignment with AI Recommendations

When you assign a sprint without specifying a team member, Stride shows AI-powered recommendations:

```bash
$ stride assign sprint-auth-system

AI-Powered Assignment Recommendations for sprint-auth-system

┌────┬────────────────────┬───────┬──────────────────────────────────────┐
│ #  │ Member             │ Score │ Reason                               │
├────┼────────────────────┼───────┼──────────────────────────────────────┤
│ 1  │ Bob Smith          │ 130   │ No current assignments (+30 bonus)   │
│ 2  │ Carol Lee          │ 115   │ Light workload (1 sprint, 20 pts)    │
│ 3  │ Alice Johnson      │ 95    │ Lead role (+15), moderate load       │
└────┴────────────────────┴───────┴──────────────────────────────────────┘

Select assignee (1-3) or enter email: 1

✓ Assigned sprint-auth-system to Bob Smith
```

**AI Scoring Factors:**

- **Workload**: Fewer current sprints = higher score
  - No assignments: +30 bonus
  - 1-2 sprints: 0 penalty
  - 3+ sprints: -20 penalty
- **Roles**: Role-based bonuses
  - Lead: +15 points
  - Developer: +5 points
- **History**: Recent assignments
  - Recent assignment: -10 penalty
- **Base Score**: 100 points

Recommendations help balance workload and leverage team expertise automatically.

### Direct Assignment

Skip AI recommendations by specifying the assignee:

```bash
stride assign sprint-auth-system --to bob@example.com
```

**With attribution:**
```bash
stride assign sprint-auth-system --to bob@example.com --by alice@example.com
```

Attribution tracks who made the assignment (useful for audit trails).

### Reassignment

Simply assign to a different member:

```bash
stride assign sprint-auth-system --to carol@example.com
```

History is preserved—metadata tracks all assignment events.

### Unassigning Sprints

```bash
stride unassign sprint-auth-system
```

**Use Cases:**
- Sprint needs to go back to backlog
- Member unavailable, need to redistribute work
- Sprint cancelled or deprioritized

---

## Workload Management

### Viewing Team Workload

See workload distribution across the entire team:

```bash
$ stride assign workload

╭─────────────── Team Workload Distribution ───────────────╮
│                                                           │
│ Team Size: 3 members                                      │
│ Total Sprints: 5                                          │
│ Average Load: 1.67 sprints/member                         │
│ Balance Score: 85/100 (Well Balanced)                     │
│                                                           │
╰───────────────────────────────────────────────────────────╯

┌────────────────────┬────────┬─────────┬──────────┬──────────────┐
│ Member             │ Active │ Pending │ Weighted │ Load Bar     │
├────────────────────┼────────┼─────────┼──────────┼──────────────┤
│ Alice Johnson      │ 2      │ 1       │ 45       │ ████████░░░░ │
│ Bob Smith          │ 1      │ 0       │ 20       │ ████░░░░░░░░ │
│ Carol Lee          │ 1      │ 0       │ 18       │ ███░░░░░░░░░ │
└────────────────────┴────────┴─────────┴──────────┴──────────────┘

Recommendations:
→ Workload is well balanced across team
→ Alice has moderate load but within acceptable range
→ Consider assigning next sprint to Bob or Carol
```

**Metrics Explained:**

- **Active**: Sprints currently in progress
- **Pending**: Proposed sprints assigned but not started
- **Weighted**: Complexity-weighted load (see below)
- **Load Bar**: Visual comparison of workload

### Complexity Scoring

Stride calculates sprint complexity to provide weighted workload:

**Formula:**
```
complexity = (stride_count × 5) + task_count
normalized to 0-100 scale (max realistic = 150 points)
```

**Example:**
- Sprint with 5 strides and 25 tasks:
  - Raw score: (5 × 5) + 25 = 50
  - Normalized: (50 / 150) × 100 = 33

**Weighted Load:**
Sum of complexity scores for all assigned sprints.

### Balance Score

Measures how evenly work is distributed:

**Formula:**
```
balance_score = 100 - (std_dev as % of mean)
```

**Interpretation:**
- **90-100**: Excellently balanced
- **70-89**: Well balanced
- **50-69**: Moderately balanced
- **<50**: Imbalanced (action needed)

### Individual Workload

View workload for a specific member:

```bash
$ stride assign workload alice@example.com

╭─────────────── Alice Johnson's Workload ───────────────╮
│                                                         │
│ Active Sprints: 2                                       │
│   • sprint-auth-system (complexity: 35)                 │
│   • sprint-api-refactor (complexity: 28)                │
│                                                         │
│ Pending Sprints: 1                                      │
│   • sprint-dashboard-ui (complexity: 22)                │
│                                                         │
│ Completed: 8 sprints                                    │
│ Total Complexity: 45/100                                │
│                                                         │
╰─────────────────────────────────────────────────────────╯
```

### Workload Recommendations

Stride automatically detects imbalance:

**Overloaded Member** (>1.5× average load):
```
⚠️  Alice is overloaded (load: 60, avg: 30)
→ Consider reassigning sprint-dashboard-ui to Bob or Carol
```

**Underutilized Member** (<0.5× average load):
```
💡 Bob is underutilized (load: 12, avg: 30)
→ Ideal candidate for next sprint assignment
```

### JSON Export

Export workload data for external analysis:

```bash
stride assign workload --export > workload.json
```

**Output format:**
```json
{
  "team_size": 3,
  "total_sprints": 5,
  "workload": [
    {
      "email": "alice@example.com",
      "name": "Alice Johnson",
      "active": 2,
      "pending": 1,
      "completed": 8,
      "weighted_load": 45
    },
    ...
  ],
  "distribution": {
    "average": 27.67,
    "min": 18,
    "max": 45,
    "std_dev": 12.34,
    "balance_score": 85
  }
}
```

---

## Approval Workflow

### Configuration

Approval policies are configured during `stride team init`:

```yaml
approval_policy:
  enabled: true                    # Enable/disable workflow
  required_approvals: 2            # N reviewers needed
  roles_can_approve:               # Role restrictions
    - lead
    - reviewer
```

**Policy Options:**

- **Disabled**: No approval required (`enabled: false`)
- **N Reviewers**: Require N approvals before completion
- **Role-Based**: Only specific roles can approve

### Approving Sprints

After a sprint is completed, team members can approve:

```bash
stride approve sprint-auth-system --by alice@example.com --comment "LGTM!"
```

**Validation:**
- Approver must have permission (role-based)
- Cannot approve own sprint (self-approval blocked)
- Cannot approve twice (duplicate prevention)

### Checking Approval Status

```bash
$ stride approve status sprint-auth-system

╭─────────────── Approval Status: sprint-auth-system ──────────────╮
│                                                                   │
│ Workflow Enabled: Yes                                             │
│ Required Approvals: 2                                             │
│ Current Approvals: 1                                              │
│                                                                   │
│ Progress: [████████████░░░░░░░░░░░░] 50% (1/2)                   │
│                                                                   │
│ Can Complete: No (1 more approval needed)                         │
│                                                                   │
╰───────────────────────────────────────────────────────────────────╯

Approvals Received:
┌───────────────────┬─────────────────────┬─────────────────────┐
│ Approver          │ Timestamp           │ Comment             │
├───────────────────┼─────────────────────┼─────────────────────┤
│ Alice Johnson     │ 2025-12-14 14:30:00 │ LGTM!               │
└───────────────────┴─────────────────────┴─────────────────────┘
```

### Listing Pending Approvals

See all sprints awaiting your approval:

```bash
$ stride approve pending --by alice@example.com

Sprints Pending Your Approval

┌──────────────────────┬──────────────────┬─────────────┬──────────┐
│ Sprint ID            │ Title            │ Assignee    │ Progress │
├──────────────────────┼──────────────────┼─────────────┼──────────┤
│ sprint-auth-system   │ Auth System      │ Bob Smith   │ 1/2      │
│ sprint-api-refactor  │ API Refactor     │ Carol Lee   │ 0/2      │
└──────────────────────┴──────────────────┴─────────────┴──────────┘
```

**Without filter** (all pending):
```bash
stride approve pending
```

### Revoking Approvals

Changed your mind? Revoke an approval:

```bash
stride approve revoke sprint-auth-system alice@example.com
```

**Use Cases:**
- Found an issue after approving
- Requirements changed
- Need more review

### Sprint Completion with Approvals

When running `/stride:complete` in your AI agent, the completion is blocked if approval threshold isn't met:

```
❌ Cannot complete sprint: Only 1/2 required approvals received

Run 'stride approve status sprint-auth-system' to see details.
```

Once threshold is met:
```
✅ Approval threshold met (2/2)
Proceeding with sprint completion...
```

---

## Comments & Communication

### Adding Comments

Add general sprint comments:

```bash
stride comment add sprint-auth-system "Great progress! Login flow is working."
```

### Code-Anchored Comments

Anchor comments to specific files and lines:

```bash
stride comment add sprint-auth-system "Consider adding rate limiting here" \
  --file src/api/auth.py \
  --line 42 \
  --by alice@example.com
```

**Benefits:**
- Precise code review feedback
- Context preserved in Git history
- Easy to locate issues

### Threaded Discussions

Reply to existing comments:

```bash
stride comment add sprint-auth-system "Done! Added rate limiting with 5 req/min" \
  --reply-to c1702573890123 \
  --by bob@example.com
```

### Viewing Comments

**Threaded view (default):**
```bash
$ stride comment list sprint-auth-system

Comments for sprint-auth-system

sprint-auth-system
├── c1702573890123 [○] Alice Johnson (src/api/auth.py:42)
│   "Consider adding rate limiting here"
│   └── c1702573891456 [✓] Bob Smith
│       "Done! Added rate limiting with 5 req/min"
└── c1702573892789 [○] Carol Lee
    "Should we add unit tests for edge cases?"
    └── c1702573893012 [○] Bob Smith
        "Good idea, I'll add them in next stride"
```

**Flat table view:**
```bash
stride comment list sprint-auth-system --flat
```

### Filtering Comments

**Show only unresolved:**
```bash
stride comment list sprint-auth-system --unresolved
```

**Show comments for specific file:**
```bash
stride comment list sprint-auth-system --file src/api/auth.py
```

### Resolving Discussions

Mark a comment as resolved:

```bash
stride comment resolve sprint-auth-system c1702573890123 --by bob@example.com
```

Reopen if needed:

```bash
stride comment unresolve sprint-auth-system c1702573890123
```

### Comment Statistics

```bash
$ stride comment stats sprint-auth-system

╭─────────────── Comment Statistics ───────────────╮
│                                                   │
│ Total Comments: 12                                │
│ Unresolved: 3                                     │
│ Resolved: 9                                       │
│                                                   │
│ Files with Comments:                              │
│ • src/api/auth.py (5 comments)                    │
│ • src/utils/validation.py (3 comments)            │
│ • tests/test_auth.py (4 comments)                 │
│                                                   │
╰───────────────────────────────────────────────────╯
```

---

## Complete Workflow Examples

### Example 1: Small Team Setup (3 Developers)

**Scenario**: A 3-person startup adopts Stride for their web app.

**Team**: Alice (lead), Bob (developer), Carol (developer)

**Steps:**

```bash
# 1. Initialize team (Alice)
stride team init
# → Project: WebApp
# → Members: Alice (lead,reviewer), Bob (developer), Carol (developer)
# → Policy: 1 required approval

# 2. Commit team config
git add .stride/team.yaml
git commit -m "Initialize Stride team collaboration"
git push

# 3. Team members sync
git pull  # Bob and Carol pull the repo

# 4. Create first sprint (Alice in AI agent)
/stride:init
/stride:plan
# → Creates sprint-user-profile

# 5. Assign to Bob with AI recommendations
stride assign sprint-user-profile
# → AI recommends Bob (no assignments), select #1

# 6. Bob implements sprint
/stride:implement
# → Works through strides, logs progress

# 7. Alice adds review comment
stride comment add sprint-user-profile "Please add input validation" \
  --file src/profile.py --line 25 --by alice@example.com

# 8. Bob resolves comment
stride comment add sprint-user-profile "Added validation" \
  --reply-to c1702573890123 --by bob@example.com
stride comment resolve sprint-user-profile c1702573890123 --by bob@example.com

# 9. Alice approves
stride approve sprint-user-profile --by alice@example.com

# 10. Bob completes sprint
/stride:complete
# → Approval threshold met, retrospective generated
```

**Outcome**: Sprint completed with full team collaboration, all tracked in Git.

---

### Example 2: Workload Balancing

**Scenario**: Team has 5 active sprints, need to assign a new one optimally.

**Steps:**

```bash
# 1. Check team workload
stride assign workload

# Output shows:
# Alice: 2 active (weighted: 45)
# Bob: 1 active (weighted: 22)
# Carol: 2 active (weighted: 40)
# Balance score: 72 (Well balanced)

# 2. Assign new sprint with AI
stride assign sprint-dashboard-redesign

# AI recommendations:
# #1 Bob Smith (130 points) - Light workload
# #2 Alice Johnson (95 points) - Lead role bonus
# #3 Carol Lee (90 points) - Moderate workload

# 3. Select Bob (#1)
# → Optimal assignment based on current workload

# 4. Verify new balance
stride assign workload
# → Balance score improved to 85
```

**Outcome**: Workload evenly distributed using AI recommendations.

---

### Example 3: Approval Workflow with 2 Reviewers

**Scenario**: Critical feature requires 2 approvals before release.

**Team**: Alice (lead), Bob (developer), Carol (reviewer), David (developer)

**Policy**: 2 required approvals, only lead and reviewer roles can approve

**Steps:**

```bash
# 1. David completes authentication sprint
/stride:implement  # David works through strides
/stride:review     # Self-review

# 2. David requests approval (via comment)
stride comment add sprint-auth-v2 "Ready for review!" --by david@example.com

# 3. Alice reviews and approves
stride comment add sprint-auth-v2 "Security looks good" \
  --file src/auth/jwt.py --line 15 --by alice@example.com
stride approve sprint-auth-v2 --by alice@example.com --comment "Approved - security validated"

# 4. Check status
stride approve status sprint-auth-v2
# → Shows 1/2 approvals (50%)

# 5. Carol reviews and finds issue
stride comment add sprint-auth-v2 "Missing rate limiting on /login endpoint" \
  --file src/api/routes.py --line 78 --by carol@example.com

# 6. David fixes and comments
stride comment add sprint-auth-v2 "Added rate limiting: 5 requests/min" \
  --reply-to c1702573894567 --by david@example.com
stride comment resolve sprint-auth-v2 c1702573894567 --by david@example.com

# 7. Carol approves after fix
stride approve sprint-auth-v2 --by carol@example.com --comment "LGTM after fix"

# 8. Check status
stride approve status sprint-auth-v2
# → Shows 2/2 approvals (100%)
# → "Can Complete: Yes"

# 9. David completes sprint
/stride:complete
# → Approval threshold met ✓
# → Retrospective generated
```

**Outcome**: Critical sprint approved by 2 reviewers with proper review cycle.

---

### Example 4: Code Review via Comments

**Scenario**: Senior dev (Alice) reviews junior dev's (Bob) code via comments.

**Steps:**

```bash
# 1. Bob completes feature sprint
/stride:implement  # Implements login feature

# 2. Alice performs code review via comments
stride comment add sprint-login "Extract this to a separate function" \
  --file src/auth.py --line 23 --by alice@example.com

stride comment add sprint-login "Use const instead of let here" \
  --file src/auth.js --line 45 --by alice@example.com

stride comment add sprint-login "Add error handling for null case" \
  --file src/auth.py --line 67 --by alice@example.com

# 3. Bob views all unresolved comments
stride comment list sprint-login --unresolved

# 4. Bob addresses each comment
stride comment add sprint-login "Refactored into validateCredentials()" \
  --reply-to c1702573895001 --by bob@example.com
stride comment resolve sprint-login c1702573895001 --by bob@example.com

stride comment add sprint-login "Changed to const" \
  --reply-to c1702573895002 --by bob@example.com
stride comment resolve sprint-login c1702573895002 --by bob@example.com

stride comment add sprint-login "Added null check with error log" \
  --reply-to c1702573895003 --by bob@example.com
stride comment resolve sprint-login c1702573895003 --by bob@example.com

# 5. Check all comments resolved
stride comment list sprint-login --unresolved
# → No unresolved comments

# 6. Alice verifies and approves
stride comment add sprint-login "All feedback addressed, great work!"
stride approve sprint-login --by alice@example.com
```

**Outcome**: Structured code review with threaded discussions, all tracked in Git.

---

### Example 5: Multi-Sprint Team Coordination

**Scenario**: Team of 4 working on parallel sprints for a major release.

**Team**: Alice (lead), Bob, Carol, David (all developers)

**Steps:**

```bash
# 1. Alice plans 4 sprints for v2.0 release
# → sprint-api-v2 (backend)
# → sprint-ui-redesign (frontend)
# → sprint-database-migration (infra)
# → sprint-test-automation (qa)

# 2. Assign based on expertise
stride assign sprint-api-v2 --to bob@example.com
stride assign sprint-ui-redesign --to carol@example.com
stride assign sprint-database-migration --to david@example.com
stride assign sprint-test-automation --to alice@example.com

# 3. Monitor team workload
stride assign workload
# → All members have 1 active sprint
# → Balance score: 100 (Perfect)

# 4. Track progress via CLI
stride list --verbose
# → Shows all 4 sprints with assignees

# 5. Team communicates via comments
stride comment add sprint-api-v2 "DB migration blocks this sprint" --by bob@example.com
stride comment add sprint-database-migration "Migration done! Bob can proceed" --by david@example.com

# 6. Alice monitors in real-time
stride status
# → Shows 4 active sprints, assignees, progress

# 7. Sprints complete in sequence
# David finishes migration first
stride approve sprint-database-migration --by alice@example.com

# Bob finishes API after migration
stride approve sprint-api-v2 --by alice@example.com

# Carol finishes UI
stride approve sprint-ui-redesign --by alice@example.com

# Alice finishes tests
stride approve sprint-test-automation --by bob@example.com

# 8. Release ready
stride metrics
# → Shows v2.0 completion metrics
```

**Outcome**: Coordinated parallel development with clear ownership and dependencies.

---

## Troubleshooting

### Common Issues

#### "team.yaml not found"

**Cause**: Team not initialized.

**Solution**:
```bash
stride team init
```

#### "Member not in team"

**Cause**: Trying to assign to email not in team.yaml.

**Solution**:
```bash
stride team add "New Member" newemail@example.com
```

#### "Permission denied: cannot approve"

**Cause**: Approver's role not in `approval_policy.roles_can_approve`.

**Solution**:
```bash
stride team edit user@example.com --roles developer,reviewer
```

#### Git Merge Conflicts in team.yaml

**Cause**: Multiple people edited team.yaml simultaneously.

**Solution**:
```bash
# 1. Resolve conflict manually in team.yaml
# 2. Ensure valid YAML structure
# 3. Test with: stride team list
# 4. Commit resolved file
```

#### Sprint Assignment Not Syncing

**Cause**: Metadata files not committed/pushed.

**Solution**:
```bash
git add .stride/sprints/*/. metadata.yaml
git commit -m "Update sprint assignments"
git push
```

---

## Best Practices

### 1. Team Configuration

✅ **Do:**
- Initialize team before first sprint assignment
- Use descriptive role combinations (e.g., lead,reviewer)
- Set realistic approval thresholds (1-2 for small teams)
- Commit team.yaml immediately after init

❌ **Don't:**
- Change email addresses (used as unique IDs)
- Remove members with active assignments
- Set approval threshold > team size

### 2. Sprint Assignment

✅ **Do:**
- Use AI recommendations for balanced distribution
- Check workload before assigning (`stride assign workload`)
- Reassign if member becomes unavailable
- Use `--by` flag for attribution in team settings

❌ **Don't:**
- Assign without checking workload
- Overload single team member
- Forget to sync assignments (git push)

### 3. Approval Workflow

✅ **Do:**
- Enable approval workflow for production releases
- Set policy based on team size (1-2 approvals typical)
- Restrict approval to experienced roles (lead, reviewer)
- Add meaningful comments with approvals

❌ **Don't:**
- Require more approvals than team capacity
- Allow self-approval (blocked by Stride)
- Skip approval for critical features

### 4. Comments & Communication

✅ **Do:**
- Anchor comments to code (use --file and --line)
- Resolve comments when addressed
- Use threading for discussions
- Check stats regularly (`stride comment stats`)

❌ **Don't:**
- Leave unresolved comments without follow-up
- Use comments for urgent issues (use direct communication)
- Forget to commit .comments.yaml

### 5. Workload Monitoring

✅ **Do:**
- Check `stride assign workload` regularly
- Aim for balance score >70
- Redistribute if members overloaded (>1.5× avg)
- Export workload data for retrospectives (`--export`)

❌ **Don't:**
- Ignore overload warnings
- Assign complex sprints to already-loaded members
- Forget complexity varies (check weighted load)

### 6. Git Workflow

✅ **Do:**
- Commit team config changes immediately
- Push metadata files after assignments
- Pull before checking team status
- Use descriptive commit messages for team changes

❌ **Don't:**
- Forget to git push after team operations
- Edit .stride/ files manually (use CLI commands)
- Force-push over team member changes

---

## Integration with Stride Lifecycle

Team collaboration integrates seamlessly with Stride's sprint lifecycle:

```
┌────────────────────────────────────────────────────┐
│ Sprint Lifecycle with Team Collaboration          │
└────────────────────────────────────────────────────┘

1. /stride:init or /stride:plan  (AI Agent)
   → Create sprint with proposal + plan

2. stride assign <sprint>  (CLI - Team Lead)
   → Assign sprint to team member with AI recommendations

3. /stride:implement  (AI Agent - Assigned Member)
   → Implement sprint with tracking

4. stride comment add  (CLI - Team Members)
   → Review and discuss implementation

5. stride approve <sprint>  (CLI - Reviewers)
   → Approve completed work (N reviewers)

6. /stride:complete  (AI Agent - Assigned Member)
   → Generate retrospective (if approval threshold met)

7. stride metrics  (CLI - Team Lead)
   → Analyze team performance and workload
```

**Key Points:**
- AI agent commands (`/stride:*`) used by assigned member
- CLI commands (`stride *`) used by team for management
- Git synchronizes all team state automatically
- Approval gates prevent premature completion

---

## Next Steps

### For Team Leads

1. **Initialize Team**: `stride team init`
2. **Configure Policy**: Set approval threshold for your team size
3. **Assign Sprints**: Use AI recommendations for balanced distribution
4. **Monitor Workload**: Regular `stride assign workload` checks
5. **Review Metrics**: Track team performance with `stride metrics`

### For Team Members

1. **Sync Team Config**: `git pull` to get team.yaml
2. **Check Assignments**: `stride list --assignee your@email.com`
3. **Implement Sprints**: Use `/stride:implement` for assigned work
4. **Provide Feedback**: Use `stride comment` for code review
5. **Give Approvals**: Use `stride approve` for peer review

### For Reviewers

1. **Check Pending**: `stride approve pending --by your@email.com`
2. **Review Code**: Use `stride comment` with file/line anchoring
3. **Verify Quality**: Check implementation logs and tests
4. **Approve**: `stride approve` when ready
5. **Track Status**: Monitor approval progress

---

## Further Reading

- [CLI Commands Reference](cli-commands.md) - Complete command documentation
- [Features Overview](features.md) - All v1.5 team features
- [Sprint Lifecycle](sprint-lifecycle.md) - Understand sprint phases
- [ROADMAP](https://github.com/saranmahadev/Stride/ROADMAP.md) - Future team features (v1.6+)

## Support

- **GitHub Issues**: https://github.com/saranmahadev/Stride/issues
- **Documentation**: https://stride.saranmahadev.in
- **Repository**: https://github.com/saranmahadev/Stride
