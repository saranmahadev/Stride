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

### v1.x (Current)

- ✅ 20 AI agents
- ✅ 6 CLI commands
- ✅ 10 agent commands
- ✅ Analytics engine

### v2.0 (Future)

- Team collaboration
- Plugin system
- Web UI (optional)
- More integrations

---

## Next Steps

- [CLI Commands →](cli-commands.md) - Learn the commands
- [Philosophy →](philosophy.md) - Understand the why
