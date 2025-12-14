# Features

Comprehensive overview of all Stride features.

---

## Multi-Agent Support

**20 AI Agents. One Unified Workflow.**

| Category | Agents |
|----------|---------|
| **AI Editors** | Cursor, Windsurf |
| **Agents** | Cline, RooCode, Factory, OpenCode, KiloCode, Antigravity |
| **Assistants** | GitHub Copilot, Amazon Q, Auggie, iFlow, CodeBuddy, Costrict |
| **CLI Tools** | Gemini CLI, Claude Code, Qoder, Qwen, Codex |
| **Specialized** | Crush |

**9 Automatic Template Formats** - Commands automatically converted for each agent's syntax

---

## Sprint Management

### Lifecycle

- **PROPOSED** → Planning phase
- **ACTIVE** → Implementation phase
- **COMPLETED** → Retrospective phase

### Features

- ✅ File-based state (no database)
- ✅ Unique sprint IDs (SPRINT-XXXXX)
- ✅ Progress tracking with strides
- ✅ Task breakdowns with checkboxes
- ✅ Real-time implementation logging

---

## Documentation System

### 6 Sprint Documents

1. **proposal.md** - What and why
2. **plan.md** - How (strides and tasks)
3. **design.md** - Architecture
4. **implementation.md** - Development log
5. **retrospective.md** - Learnings
6. **project.md** - Project overview

### Benefits

- Version control friendly
- Human and AI readable
- No databases required
- Easy backup and restore

---

## CLI Commands

### `stride init`
Initialize project with agent selection

### `stride list`
View all sprints with status badges

### `stride status`
Check current project state

### `stride show`
Detailed sprint information

### `stride validate`
Verify project structure

### `stride metrics`
Analytics and insights with JSON/CSV export

---

## Agent Commands

### `/stride:init`
Create project spec and first sprint

### `/stride:plan`
Break down goals into strides and tasks

### `/stride:implement`
Build features with logging

### `/stride:status`
Check sprint progress

### `/stride:review`
Validate work quality

### `/stride:complete`
Archive sprint with retrospective

### `/stride:present`
Generate presentations

### `/stride:derive`
Create sprint from existing

### `/stride:lite`
Quick command reference

### `/stride:feedback`
Collect and organize feedback

---

## Progress Tracking

### Strides (Milestones)

```markdown
## Stride 1: Database Schema
- [x] Create tables
- [x] Add indexes
- [x] Write migrations

## Stride 2: API Endpoints
- [x] Register endpoint
- [ ] Login endpoint   ← Currently here
- [ ] Logout endpoint
```

### Acceptance Criteria

```markdown
- [x] Users can register
- [ ] Users can login
- [ ] Users can logout
```

### Implementation Logs

Timestamped entries tracking:
- Tasks addressed
- Decisions made
- Code changes
- Notes and observations

---

## Analytics Engine

### Sprint Metrics

- Duration tracking
- Completion rates
- Task distribution
- Process compliance scoring
- Quality indicators

### Export Options

- JSON format
- CSV format
- Per-sprint or aggregate

---

## Template Conversion

**9 Format Types:**

1. `yaml-rich-metadata` - Claude, CodeBuddy, Crush, Qoder
2. `yaml-name-id` - Cursor, iFlow
3. `yaml-arguments` - Codex, Auggie, Factory
4. `yaml-xml-tags` - Amazon Q, OpenCode
5. `yaml-auto-exec` - Windsurf
6. `yaml-github-copilot` - GitHub Copilot
7. `toml` - Qwen, Gemini, Codex
8. `markdown-heading` - Cline, RooCode
9. `no-frontmatter` - KiloCode

**Automatic conversion** during `stride init`

---

## Terminal UI

### Beautiful Output

- Color-coded status badges
- ASCII progress bars
- Rich table displays
- Interactive prompts
- Spinners and animations
- ASCII art branding

### Colors

- **PROPOSED** - Yellow
- **ACTIVE** - Blue
- **COMPLETED** - Green

---

## Technical Specifications

### Architecture

- **CLI Framework**: Typer
- **Terminal UI**: Rich
- **Data Models**: Pydantic v2
- **Parser**: Custom markdown parser
- **Template Engine**: 9-format converter

### Python Support

- Python 3.8+
- Windows, macOS, Linux

### Dependencies

- typer[all]
- rich
- pyyaml
- pydantic
- pyfiglet
- questionary

---

## Security & Privacy

- ✅ No external API calls
- ✅ All data stored locally
- ✅ No telemetry
- ✅ No account required
- ✅ Works offline

---

## Performance

- ⚡ Fast startup (<100ms)
- ⚡ Instant command execution
- ⚡ Efficient markdown parsing
- ⚡ Minimal memory footprint
- ⚡ No background processes

---

## Extensibility

### Adding New Agents

Simple configuration in `agent_registry.py`:

```python
"new-agent": AgentConfig(
    name="New Agent",
    key="new-agent",
    directory=".newagent/commands",
    extension=".md",
    format_type="yaml-rich-metadata",
)
```

### Custom Templates

Edit templates in `stride/templates/`

### Plugins (Future)

Plugin system planned for v2.0

---

## Team Collaboration (v1.5)

**Git-Based, Zero-Infrastructure Team Workflows**

### Philosophy

Stride v1.5 introduces team collaboration without external services:

- **Repo-First** - All data stored in `.stride/team.yaml`
- **Zero-Infrastructure** - No servers, databases, or accounts
- **Git-Powered** - Use your existing Git workflow
- **Privacy-First** - Team data stays in your repository

### Features

#### 🏢 Team Management

```bash
stride team init              # Initialize team configuration
stride team add <name> <email> --role <role>
stride team remove <email>
stride team edit <email>
stride team list              # View all members + workload
stride team show <email>      # Detailed member info
```

**Roles:** developer, reviewer, lead

#### 🎯 Sprint Assignment

```bash
stride assign <sprint-id>     # AI-powered recommendations
stride assign direct <sprint-id> <email>
stride assign reassign <sprint-id> <email>
```

**AI Recommendations** analyze:
- Current workload distribution
- Skill/expertise match (from history)
- Sprint complexity
- Team balance score

#### ✅ Approval Workflows

```bash
stride approve config <1|2>   # Require 1 or 2 approvals
stride approve <sprint-id>
stride approve status <sprint-id>
stride approve pending        # View sprints awaiting your approval
stride approve revoke <sprint-id>
```

**Policies:**
- **1-approval:** Any single reviewer can approve
- **2-approval:** Requires two independent reviewers

#### 💬 Comments & Code Review

```bash
stride comment add <sprint-id> <text>
stride comment code <sprint-id> <file> <line> <text>
stride comment reply <sprint-id> <comment-id> <text>
stride comment resolve <sprint-id> <comment-id>
stride comment list <sprint-id>
stride comment stats <sprint-id>
```

**Features:**
- General and code-anchored comments
- Threaded discussions
- Resolution tracking
- Author attribution

#### ⚖️ Workload Balancing

```bash
stride metrics --team         # View team workload
stride team list              # Balance score + distribution
```

**Complexity Scoring:**
```
workload = (stride_count × 5) + task_count
```

**Balance Score:**
```
balance = 100 - (std_dev as % of mean)
```

Higher balance score = more evenly distributed work

#### 📊 Enhanced Commands

```bash
stride list --assignee <email>   # Filter by assignee
stride metrics --team            # Team workload metrics
stride show <sprint-id>          # Shows assignee + approvals
```

### Workflow Examples

#### Small Team Setup

```bash
# 1. Initialize team
stride team init

# 2. Add members
stride team add "Alice" "alice@example.com" --role lead
stride team add "Bob" "bob@example.com" --role developer

# 3. Assign sprint with AI
stride assign sprint-auth

# 4. Approve when ready
stride approve sprint-auth --comment "LGTM!"
```

#### Code Review Process

```bash
# 1. Add code comment
stride comment code sprint-auth src/auth.py 42 "Consider using bcrypt"

# 2. Developer replies
stride comment reply sprint-auth c1 "Good catch! Will update."

# 3. Resolve after fix
stride comment resolve sprint-auth c1

# 4. Approve sprint
stride approve sprint-auth
```

### Architecture

**File Structure:**
```
.stride/
  team.yaml           # Team configuration + member list
  sprints/
    sprint-abc123/
      plan.md         # Includes assignee field
      ...
```

**team.yaml Format:**
```yaml
approval_policy: 2
members:
  - name: Alice
    email: alice@example.com
    role: lead
assignments:
  sprint-abc123:
    assignee: alice@example.com
    approvals:
      - reviewer: bob@example.com
        timestamp: 2024-12-14T10:30:00
        comment: "LGTM!"
    comments:
      - id: c1
        author: bob@example.com
        text: "Great work!"
        timestamp: 2024-12-14T09:00:00
        resolved: false
```

### Backward Compatibility

- **100% Optional** - All team commands are opt-in
- **Solo Mode** - Works exactly as before without `team.yaml`
- **Progressive Adoption** - Add team features incrementally
- **No Breaking Changes** - Existing sprints unaffected

[Learn More →](team-workflow.md){ .md-button }

---

## Comparison

### vs Manual Documentation

| Feature | Manual | Stride |
|---------|--------|--------|
| Structure | ❌ Inconsistent | ✅ Consistent |
| Tracking | ❌ Manual | ✅ Automatic |
| Analytics | ❌ None | ✅ Built-in |
| Multi-agent | ❌ No | ✅ 20 agents |

### vs Project Management Tools

| Feature | PM Tools | Stride |
|---------|----------|--------|
| AI Native | ❌ No | ✅ Yes |
| Local-first | ❌ Cloud | ✅ Local |
| Version Control | ❌ Separate | ✅ Integrated |
| Setup | ❌ Complex | ✅ One command |

---

## Roadmap

### v1.5 (Current) ✨

- ✅ 20 AI agents
- ✅ Team collaboration
- ✅ Workload balancing
- ✅ Approval workflows
- ✅ Code review system

### v2.0 (Future)

- Plugin system
- Web UI (optional)
- More integrations
- Advanced analytics

---

## Next Steps

- [CLI Commands →](cli-commands.md) - Learn the commands
- [Philosophy →](philosophy.md) - Understand the why
