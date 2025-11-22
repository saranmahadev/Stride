# **Stride**# **Stride**



> **Sprint-Powered, Spec-Driven Development for AI Agents**> **Sprint-Powered, Spec-Driven Development for AI Agents**



------



**Stride** is a **sprint-powered, spec-driven development engine** that turns AI agents into reliable product teams—delivering features, not just code.**Stride** is the **sprint-powered, spec-driven development engine** that turns AI agents into reliable product teams—delivering features, not just code.



We combine **agile velocity**, **spec-first discipline**, and **multi-agent coordination** into a unified workflow for:We combine **OpenSpec’s clarity**, **SpecKit’s rigor**, and **agile velocity** into a unified workflow that works for:

- Solo indie hackers shipping MVPs- Solo indie hackers shipping MVPs

- Small teams iterating on greenfield apps- Small teams iterating on greenfield apps

- Developers working with AI coding assistants- Enterprises retrofitting legacy systems



**Mission:** Make AI-assisted development *predictable*, *auditable*, and *fast* without meetings, without drift, without rework.**Mission:** Make AI-assisted development *predictable*, *auditable*, and *fast* without meetings, without drift, without rework.



------



## **Core Principles**## **2. Core Principles**



| Principle | Description || Principle | Description |

|--------|-------------||--------|-------------|

| **Spec-First, Sprint-Second** | Every change starts with a locked spec; every spec becomes a time-boxed sprint. || **Spec-First, Sprint-Second** | Every change starts with a locked spec; every spec becomes a time-boxed sprint. |

| **Agent-Agnostic** | Works with 20+ AI coding agents: Claude, Cursor, Windsurf, GitHub Copilot, Cline, and more. || **Agent-Agnostic** | Works with any Coding Agents such as Claude Code, Github Copilot, Gemini CLI, Kilo Code. |

| **Human-in-the-Loop** | Feedback is a first-class command; track changes and maintain control. || **Human-in-the-Loop** | Feedback is a first-class command; AI learns, adapts, and improves. |

| **Status-Driven Workflow** | Visual sprint management through folder-based status transitions. || **Lightweight by Default, Rigorous on Demand** | Lite mode for quick fixes; full validation for production. |

| **Living Artifacts** | Specs, plans, and code evolve together—never stale. || **Living Artifacts** | Specs, plans, and code evolve together—never stale. |



------



## **Target Users**## **3. Target Users**



| Persona | Pain Point | Stride Solution || Persona | Pain Point | Stride Solution |

|-------|-----------|-----------------||-------|-----------|-----------------|

| **Indie Hacker** | "AI writes code, but I lose context in 3 chats." | `stride init` → sprint → ship in one flow || **Indie Hacker** | "AI writes code, but I lose context in 3 chats." | `/stride:init` → sprint → ship in one flow |

| **Startup CTO** | "We use Cursor + Claude, but outputs don't align." | Multi-agent workflow + unified tasks || **Startup CTO** | "We use Cursor + Claude, but outputs don’t align." | `AGENTS.md` + `/stride:plan` → unified tasks |

| **AI-First Developer** | "Need to track what AI agents actually implemented." | Sprint history + validation + exports || **Enterprise Dev Lead** | "Can’t trust AI in legacy repos." | `/stride:introspect` + validation pipelines |



------



## **Key Features**## **4. Key Features**



### AI Agent Commands (In-Editor)### AI Agent Commands (In-Editor)



Stride integrates with 20 AI coding agents through native slash commands:| Feature | Command | Description | Inspired By |

|-------|--------|-------------|-------------|

| Command | Description || **Project Initialization** | `/stride:init` | Initialize project context and introspect repository | Stride Original |

|---------|-------------|| **Sprint Planning** | `/stride:plan <feature>` | Creates sprint in `proposed/` with tasks, estimates, risks | Stride + SpecKit |

| `/stride:init` | Initialize project context || **Plan Presentation** | `/stride:present <ID>` | Renders plan as Markdown + Mermaid diagrams | Stride |

| `/stride:plan <feature>` | Create sprint with tasks and estimates || **Automated Implementation** | `/stride:implement <ID>` | Moves to `active/`, executes sprint, outputs notes | Stride + OpenSpec |

| `/stride:present <ID>` | View plan with diagrams || **Real-Time Feedback** | `/stride:feedback <ID> "note"` | Agent corrects course, updates plan mid-sprint | Stride Original |

| `/stride:implement <ID>` | Execute sprint implementation || **Sprint Blocking** | `/stride:block <ID> "reason"` | Moves to `blocked/` folder, tracks impediments | Agile Workflows |

| `/stride:feedback <ID> "note"` | Apply real-time corrections || **Sprint Unblocking** | `/stride:unblock <ID>` | Returns sprint to `active/` folder | Agile Workflows |

| `/stride:block <ID> "reason"` | Mark sprint as blocked || **Review Submission** | `/stride:submit <ID>` | Moves to `review/` for testing/approval | Agile Workflows |

| `/stride:unblock <ID>` | Resume blocked sprint || **Sprint Closure** | `/stride:complete <ID>` | Moves to `completed/`, merges specs, creates retrospective | OpenSpec + Stride |

| `/stride:submit <ID>` | Submit for review |

| `/stride:complete <ID>` | Finalize and archive sprint |### CLI Commands (Terminal)



**Supported AI Agents (20):**| Feature | Command | Description | Inspired By |

- **High Priority:** Claude Code, Cursor, Windsurf, GitHub Copilot, Cline|-------|--------|-------------|-------------|

- **Medium Priority:** Auggie, RooCode, CodeBuddy, CoStrict, Crush, Factory Droid, Gemini CLI, OpenCode| **Framework Setup** | `stride init` | Initialize Stride framework and configure AI agents | Stride Original |

- **Low Priority:** Kilo Code, Qoder, Antigravity, Codex, Amazon Q Developer, Qwen Code| **User Authentication** | `stride login` | Authenticate for sprint authorship tracking | Team Workflows |

- **Universal:** Fallback AGENTS.md for any tool| **Status Dashboard** | `stride status` | Sprint distribution and team analytics | Agile Dashboards |

| **Progress Monitoring** | `stride progress <ID>` | Detailed sprint progress with task breakdown | Stride Original |

### CLI Commands (Terminal)| **Live Monitoring** | `stride watch <ID>` | Real-time sprint implementation streaming | DevOps Workflows |

| **Sprint Timeline** | `stride timeline <ID>` | Complete activity history with timestamps | Audit Trails |

Complete command-line interface for sprint management:| **Sprint Listing** | `stride list` | List/filter sprints by status, user, or date | Project Management |

| **Sprint Details** | `stride show <ID>` | Display complete sprint information | Stride Original |

| Category | Commands | Description || **Spec Comparison** | `stride diff <ID>` | Show specification changes made in sprint | Git Workflows |

|----------|----------|-------------|| **Quality Validation** | `stride validate <ID>` | Comprehensive sprint quality validation with detailed reports | CI/CD Pipelines |

| **Setup** | `init`, `login`, `logout`, `whoami` | Framework initialization and authentication || **Agent Management** | `stride agent` | Manage AI agents for your project | AI Integration |

| **Sprint Management** | `create`, `list`, `show`, `status`, `move` | Core sprint operations || **Configuration** | `stride config` | Manage project and user settings | Stride Original |

| **Monitoring** | `progress`, `watch`, `timeline` | Real-time sprint tracking || **Health Check** | `stride doctor` | Validate installation and project health | Package Managers |

| **Quality** | `validate`, `doctor` | Health checks and validation || **Data Export** | `stride export` | Export sprint data for reporting/integration | Enterprise Tools |

| **Maintenance** | `archive`, `restore`, `export` | Sprint lifecycle and reporting || **Updates** | `stride update` | Update Stride framework to latest version | Package Managers |

| **Configuration** | `config` (init/get/set/list/validate/reset) | Settings management |

| **AI Agents** | `agent` (list/add/remove/info/init/update/validate) | Multi-agent coordination |---



---## **5. Advanced Features**



## **Quick Start**| Feature | Description | Priority |

|-------|-------------|----------|

### Installation| **Lite Mode** | `/stride:lite "Add dark mode"` → plan + implement in <200 lines | High |

| **User Authentication** | `stride login` → track authorship and team activity | High |

```bash| **Live Monitoring** | `stride watch <ID>` → real-time sprint progress streaming | High |

# Clone the repository| **Status Dashboard** | `stride status` → team analytics and sprint distribution | High |

git clone https://github.com/saranmahadev/Stride.git| **Validation Pipelines** | `stride validate` → auto-run tests, lint, semantic checks | High |

cd Stride| **Sprint Timeline** | `stride timeline <ID>` → complete activity history | High |

| **Introspection Engine** | AI scans legacy code → generates migration sprints | High |

# Create virtual environment| **Auto-Retrospectives** | AI generates retrospectives on `/stride:complete` | Medium |

python -m venv venv| **Blocker Analytics** | Track time in `blocked/`, common impediments via `stride status` | Medium |

source venv/bin/activate  # Windows: venv\Scripts\activate| **Export & Reporting** | `stride export` → Markdown/HTML/JSON reports for stakeholders | Medium |

| **Health Monitoring** | `stride doctor` → validate installation and project health | Medium |

# Install dependencies| **Provenance Scores** | 0–100 badge: "Spec Alignment: 94%" | Low |

pip install -r requirements.txt

---

# Verify installation

stride --version## **6. CLI Quick Start**

```

### Installation

### Your First Sprint

```bash

```bash# Clone the repository

# 1. Initialize Stride in your projectgit clone https://github.com/yourusername/stride.git

cd your-projectcd stride

stride init

# Create virtual environment

# 2. Configure AI agents you're usingpython -m venv venv

stride agent initsource venv/bin/activate  # On Windows: venv\Scripts\activate

# Select: Claude, Cursor, Windsurf (interactive wizard)

# Install dependencies

# 3. Create a new sprintpip install -r requirements.txt

stride create --title "Add user authentication" --priority high

# Output: ✓ Created: SPRINT-7K9P# Verify installation

python -m stride.cli.main --version

# 4. Move to active and start working```

stride move SPRINT-7K9P active

### Your First Sprint

# 5. Monitor progress in real-time

stride watch SPRINT-7K9P```bash

# 1. Initialize Stride in your project

# 6. Check sprint statuscd your-project

stride status SPRINT-7K9Ppython -m stride.cli.main init

stride timeline SPRINT-7K9P

# 2. Create a new sprint

# 7. Validate quality before completionpython -m stride.cli.main create \

stride validate SPRINT-7K9P --detailed  --title "Add user authentication" \

  --tags "feature,security" \

# 8. Complete the sprint  --priority high

stride move SPRINT-7K9P completed

```# Output: ✓ Created: SPRINT-7K9P



### AI Agent Workflow# 3. Start working on it

python -m stride.cli.main move SPRINT-7K9P active

After running `stride agent init`, use these commands in your AI coding assistant:

# 4. Check status anytime

```bashpython -m stride.cli.main status SPRINT-7K9P

# In Claude Code, Cursor, Windsurf, etc.

/stride:init              # Understand project context# 5. View complete sprint details

/stride:plan "Add login"  # Create detailed sprint planpython -m stride.cli.main show SPRINT-7K9P

/stride:implement SPRINT-7K9P  # Execute implementation

/stride:feedback SPRINT-7K9P "Use bcrypt for passwords"  # Apply changes# 6. View a specific document (proposal, plan, design, implementation, retrospective)

/stride:complete SPRINT-7K9P   # Finalize workpython -m stride.cli.main show SPRINT-7K9P --file proposal

```

# 7. List all active sprints

---python -m stride.cli.main list --status active



## **Technical Architecture**# 8. Filter sprints by author

python -m stride.cli.main list --user alice@example.com

### Sprint Status Workflow

# 9. Sort sprints by priority

```python -m stride.cli.main list --sort priority

proposed/ → active/ → blocked/ → review/ → completed/ → .archive/

```# 10. Validate your work (basic)

python -m stride.cli.main validate SPRINT-7K9P

Sprints move through clearly defined status folders, providing visual tracking and git-friendly state management.

# 10a. Validate with detailed quality report

### Folder Structurepython -m stride.cli.main validate SPRINT-7K9P --detailed



```# 10b. Validate all sprints

your-project/python -m stride.cli.main validate --all

├── stride/

│   ├── sprints/# 11. View sprint timeline (event history)

│   │   ├── proposed/    # New sprint ideaspython -m stride.cli.main timeline SPRINT-7K9P

│   │   ├── active/      # In-progress work

│   │   ├── blocked/     # Waiting on dependencies# 12. Show recent 5 events only

│   │   ├── review/      # Pending approvalpython -m stride.cli.main timeline SPRINT-7K9P --limit 5

│   │   ├── completed/   # Finished sprints

│   │   └── .archive/    # Archived sprints# 13. Watch sprint for real-time file changes

│   ├── specs/           # Specification documentspython -m stride.cli.main watch SPRINT-7K9P

│   ├── config/          # Project configuration

│   └── project.md       # Project context# 13a. Watch with custom refresh interval

├── CLAUDE.md            # Claude Code integrationpython -m stride.cli.main watch SPRINT-7K9P --interval 0.5

├── CURSOR.md            # Cursor integration

└── .windsurf/           # Windsurf workflows# 14. Run health check on project

```python -m stride.cli.main doctor



### Technology Stack# 14a. Get detailed health check output

python -m stride.cli.main doctor --verbose

- **Language:** Python 3.11+

- **CLI Framework:** Click# 14b. Export health report as JSON for CI/CD

- **Configuration:** YAML (project) + TOML (agents)python -m stride.cli.main doctor --json > health-report.json

- **Templates:** Jinja2

- **Output:** Rich (terminal UI)# 15. Manage AI agents

- **Testing:** pytest (454 tests, 73% coverage)python -m stride.cli.main agent list



---# 15a. Add AI agent to track which tools you use

python -m stride.cli.main agent add claude

## **Advanced Features**

# 15b. Get details about an agent

| Feature | Description | Status |python -m stride.cli.main agent info copilot

|---------|-------------|--------|

| **User Authentication** | Track authorship with `stride login` | ✅ Implemented |# 15c. Remove an agent

| **Live Monitoring** | Real-time sprint progress with `stride watch` | ✅ Implemented |python -m stride.cli.main agent remove claude

| **Multi-Agent Support** | 20 AI tools with unified workflows | ✅ Implemented |

| **Validation Pipelines** | Comprehensive quality checks | ✅ Implemented |# 16. Export sprint data for reporting

| **Sprint Timeline** | Complete activity history | ✅ Implemented |python -m stride.cli.main export --format markdown --output report.md

| **Export & Reporting** | JSON/Markdown/CSV/HTML reports | ✅ Implemented |

| **Health Monitoring** | `stride doctor` for project health | ✅ Implemented |# 16a. Export completed sprints as JSON

| **Configuration System** | User + project-level settings | ✅ Implemented |python -m stride.cli.main export --format json --status completed --output completed-sprints.json



---# 16b. Export HTML report with filters

python -m stride.cli.main export --format html --since 2025-01-01 --priority high --output high-priority-report.html

## **Command Reference**

# 17. Move to review when ready

For detailed documentation of all commands, see **[COMMANDS.md](COMMANDS.md)**.python -m stride.cli.main move SPRINT-7K9P review



### Most Used Commands# 18. Complete the sprint

python -m stride.cli.main move SPRINT-7K9P completed

```bash```

# Setup

stride init                        # Initialize framework### Complete Command Reference

stride login                       # Authenticate user

stride agent init                  # Configure AI agentsFor detailed documentation of all CLI commands, options, and examples, see **[COMMANDS.md](COMMANDS.md)**.



# Sprint OperationsKey commands:

stride create --title "Feature"    # Create new sprint- `init` - Initialize Stride in a project

stride list --status active        # List active sprints- `create` - Create new sprints

stride move SPRINT-ID active       # Change sprint status- `list` - List and filter sprints (with --user, --since, --until, --sort options)

stride validate SPRINT-ID          # Check sprint quality- `show` - Display complete sprint details with file viewer

- `status` - Show sprint metadata

# Monitoring- `timeline` - View complete event history with timestamps

stride status                      # Dashboard overview- `watch` - Monitor sprint for real-time file changes with live display

stride watch SPRINT-ID             # Live monitoring- `move` - Change sprint status

stride timeline SPRINT-ID          # Activity history- `validate` - Comprehensive sprint quality validation with detailed reports

stride progress SPRINT-ID          # Task completion- `archive` - Archive completed sprints

- `restore` - Restore archived sprints

# Reporting

stride export --format markdown    # Generate reports---

stride doctor                      # Health check

```## **7. Technical Architecture**



---```

┌─────────────────────┐

## **Development Status**│   Agent Interface   │

│  (Claude Code,      |

### v1.0 Release (Ready)│   Gemini CLI, Github|

|       Copilot       │

**Test Coverage:**└───────┬─────────────┘

- 454 tests passing        │ /stride:*

- 73% code coverage        │

- Zero known critical bugs        │

        ▼

**Completed Features:**┌─────────────────────┐

- ✅ Complete CLI suite (18 commands)│   LLM Backends      │

- ✅ Sprint lifecycle management│  (Claude, Gemini,   │

- ✅ Multi-agent integration (20 tools)│   Grok, Local, etc.)│

- ✅ User authentication└───────┬─────────────┘

- ✅ Configuration system        │

- ✅ Validation & health checks        ▼

- ✅ Export & reporting┌─────────────────────┐

- ✅ Real-time monitoring│ Status-Based Folders│

│  • proposed/        │

---│  • active/          │

│  • blocked/         │

## **Roadmap**│  • review/          │

│  • completed/       │

### Future Enhancements (Post v1.0)└─────────────────────┘

```

| Feature | Priority | Target |

|---------|----------|--------|- **State**: Status-based folder structure (git-tracked)

| **Diff Command** | High | v1.1 |- **Specs**: Markdown + YAML frontmatter in `stride/specs/`

| **Framework Update Command** | High | v1.1 |- **Sprints**: Organized by lifecycle state in `stride/sprints/`

| **Auto-Retrospectives** | Medium | v1.2 |- **Metadata**: Frontmatter tracks dates, status, completion

| **VS Code Extension** | Medium | v1.3 |- **Extensible**: Plugins via `stride.config.js`

| **Introspection Engine** | Low | v2.0 |

| **Lite Mode** | Low | v2.0 |### Sprint Workflow Diagram

| **Provenance Scores** | Low | v2.0 |

| **CI/CD Integrations** | Medium | v1.4 |```mermaid

| **Team Collaboration** | Medium | v1.5 |graph TD

    Start([Developer Starts Feature]) --> Init[/stride:init<br/>Initialize Context/]

See **[ROADMAP.md](ROADMAP.md)** for detailed planning.    Init --> Plan[/stride:plan<br/>Create Sprint Plan/]

    Plan --> Proposed[(proposed/<br/>SPRINT-ID)]

---    

    Proposed --> Review{Human<br/>Review?}

## **Competitive Position**    Review -->|Approve| Present[/stride:present<br/>View Plan/]

    Review -->|Reject| Revise[Revise Plan]

**Stride vs Traditional Tools:**    Revise --> Proposed

    

| | **OpenSpec** | **SpecKit** | **Stride v1.0** |    Present --> Implement[/stride:implement<br/>Execute Sprint/]

|---|--------------|-------------|-----------------|    Implement --> Active[(active/<br/>SPRINT-ID)]

| **Greenfield** | Good | Weak | Excellent |    

| **Speed** | Medium | Slow | Fast |    Active --> Progress{Check<br/>Progress}

| **Rigor** | Medium | High | High |    Progress -->|Monitor| Watch[stride watch<br/>Live Updates]

| **Feedback Loop** | Weak | Weak | Excellent |    Progress -->|Status| StatusCmd[stride status<br/>Dashboard]

| **Multi-Agent** | Excellent | Medium | Excellent (20 tools) |    Watch --> Active

| **Status Tracking** | Weak | Weak | Excellent |    StatusCmd --> Active

| **Live Monitoring** | None | None | Built-in |    

| **CLI Tools** | Limited | Limited | Comprehensive (18 commands) |    Active --> Feedback{Need<br/>Changes?}

| **Reporting** | Weak | Medium | Excellent |    Feedback -->|Yes| ApplyFeedback[/stride:feedback<br/>Apply Corrections/]

    ApplyFeedback --> Active

**Stride = OpenSpec's portability + SpecKit's validation + Agile velocity + DevOps monitoring**    

    Active --> BlockCheck{Blocked?}

---    BlockCheck -->|Yes| Block[/stride:block<br/>Mark Blocked/]

    Block --> Blocked[(blocked/<br/>SPRINT-ID)]

## **Contributing**    Blocked --> Unblock[/stride:unblock<br/>Resume Sprint/]

    Unblock --> Active

Stride is open for contribution. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.    

    BlockCheck -->|No| Feedback

### Development Setup    Feedback -->|No| Submit[/stride:submit<br/>Submit for Review/]

    Submit --> ReviewFolder[(review/<br/>SPRINT-ID)]

```bash    

# Install development dependencies    ReviewFolder --> Validate[stride validate<br/>Quality Check]

pip install -r requirements.txt    Validate --> TestReview{Tests<br/>Pass?}

pip install -e .    TestReview -->|Fail| FixIssues[Fix Issues]

    FixIssues --> Active

# Run tests    

pytest tests/ -v    TestReview -->|Pass| Complete[/stride:complete<br/>Finalize Sprint/]

    Complete --> Completed[(completed/<br/>SPRINT-ID)]

# Check coverage    Completed --> Retro[Auto-Generate<br/>Retrospective]

pytest tests/ --cov=stride --cov-report=html    Retro --> MergeSpecs[Merge Spec Deltas<br/>to stride/specs/]

```    MergeSpecs --> Export[stride export<br/>Generate Reports]

    Export --> End([Sprint Completed])

---    

    style Start fill:#e1f5e1

## **License**    style End fill:#e1f5e1

    style Proposed fill:#fff4e6

MIT License - see [LICENSE](LICENSE) for details.    style Active fill:#e3f2fd

    style Blocked fill:#ffebee

---    style ReviewFolder fill:#f3e5f5

    style Completed fill:#e8f5e9

## **Quick Reference Card**    style Block fill:#ff6b6b

    style Complete fill:#51cf66

### AI Agent Commands```

```

/stride:init                       # Initialize context### CLI Monitoring Flow

/stride:plan "feature"             # Create sprint

/stride:implement SPRINT-ID        # Execute sprint```mermaid

/stride:feedback SPRINT-ID "note"  # Apply correctionsgraph LR

/stride:complete SPRINT-ID         # Finalize    User([Developer]) --> CLI{Stride CLI}

```    

    CLI --> Setup[Setup Commands]

### CLI Commands    Setup --> Init[stride init]

```    Setup --> Login[stride login]

stride init                        # Setup framework    

stride agent init                  # Configure AI tools    CLI --> Monitor[Monitoring Commands]

stride create --title "Feature"    # New sprint    Monitor --> StatusCmd[stride status]

stride watch SPRINT-ID             # Live monitor    Monitor --> Progress[stride progress]

stride validate SPRINT-ID          # Quality check    Monitor --> Watch[stride watch]

stride export                      # Generate reports    Monitor --> Timeline[stride timeline]

```    Monitor --> List[stride list]

    

---    CLI --> Quality[Quality Commands]

    Quality --> Validate[stride validate]

> **"Code is easy. Shipping is hard. Stride makes shipping inevitable."**      Quality --> Diff[stride diff]

> — *Stride v1.0*    

    CLI --> Config[Configuration]
    Config --> ConfigCmd[stride config]
    Config --> Doctor[stride doctor]
    
    CLI --> Maint[Maintenance]
    Maint --> Export[stride export]
    Maint --> Update[stride update]
    
    StatusCmd --> Dashboard[(Dashboard<br/>Analytics)]
    Progress --> Details[(Sprint<br/>Progress)]
    Watch --> Live[(Live<br/>Stream)]
    Timeline --> History[(Activity<br/>Log)]
    List --> Filtered[(Filtered<br/>Sprints)]
    
    Validate --> Score[(Quality<br/>Score)]
    Diff --> Changes[(Spec<br/>Changes)]
    
    Export --> Reports[(Reports<br/>JSON/MD/HTML)]
    
    style User fill:#e1f5e1
    style Dashboard fill:#e3f2fd
    style Details fill:#e3f2fd
    style Live fill:#fff4e6
    style History fill:#f3e5f5
    style Score fill:#e8f5e9
    style Reports fill:#fff9c4
```

### Multi-Agent Integration

```mermaid
graph TD
    Stride[Stride Framework] --> Agents{AI Agent Layer}
    
    Agents --> Claude[Claude Code]
    Agents --> Copilot[GitHub Copilot]
    Agents --> Windsurf[Windsurf]
    Agents --> Gemini[Gemini CLI]
    Agents --> Kilo[Kilo Code]
    Agents --> Other[Other Agents]
    
    Claude --> AgentConfig[AGENTS.md<br/>Configuration]
    Copilot --> AgentConfig
    Windsurf --> AgentConfig
    Gemini --> AgentConfig
    Kilo --> AgentConfig
    Other --> AgentConfig
    
    AgentConfig --> Commands[Slash Commands<br/>/stride:*]
    
    Commands --> ProjectContext[stride/project.md<br/>Project Context]
    Commands --> Specs[stride/specs/<br/>Specifications]
    Commands --> Sprints[stride/sprints/<br/>Status Folders]
    
    Sprints --> Proposed[(proposed/)]
    Sprints --> Active[(active/)]
    Sprints --> Blocked[(blocked/)]
    Sprints --> Review[(review/)]
    Sprints --> Completed[(completed/)]
    
    style Stride fill:#667eea,color:#fff
    style AgentConfig fill:#764ba2,color:#fff
    style Commands fill:#f093fb
    style Proposed fill:#fff4e6
    style Active fill:#e3f2fd
    style Blocked fill:#ffebee
    style Review fill:#f3e5f5
    style Completed fill:#e8f5e9
```

---

## **7. File Structure (Status-Driven)**

```bash
my-project/
├── stride/
│   ├── project.md                   # Project context, conventions, tech stack
│   ├── AGENTS.md                    # Multi-tool config (Claude, Cursor, etc.)
│   │
│   ├── specs/                       # Living specifications (current state)
│   │   ├── auth/
│   │   │   └── spec.md
│   │   ├── payments/
│   │   │   └── spec.md
│   │   └── ...
│   │
│   ├── sprints/
│   │   ├── proposed/                # Pending review/approval
│   │   │   └── SPRINT-7K9P/
│   │   │       ├── proposal.md
│   │   │       └── plan.md
│   │   │
│   │   ├── active/                  # Currently being worked on
│   │   │   └── SPRINT-5A2B/
│   │   │       ├── proposal.md
│   │   │       ├── plan.md
│   │   │       ├── design.md
│   │   │       ├── implementation.md
│   │   │       ├── feedback.log
│   │   │       └── specs/           # Spec deltas
│   │   │           └── auth/
│   │   │               └── spec.md
│   │   │
│   │   ├── blocked/                 # Waiting on dependencies/decisions
│   │   │   └── SPRINT-3X8Y/
│   │   │
│   │   ├── review/                  # Implementation done, pending verification
│   │   │   └── SPRINT-2M4N/
│   │   │
│   │   └── completed/               # Shipped and merged
│   │       └── SPRINT-6C4D/
│   │           ├── proposal.md
│   │           ├── plan.md
│   │           ├── implementation.md
│   │           ├── retrospective.md  # What went well/poorly
│   │           └── specs/
│   │
│   │
│   └── introspection/               # Legacy code analysis
│       ├── scan-results.json
│       └── migration-candidates.md 
```

### Sprint Lifecycle States

| Status | Description | Typical Duration | Commands |
|--------|-------------|------------------|----------|
| **proposed/** | Sprint planned but not started | Hours to days | `/stride:plan` → creates here |
| **active/** | Currently being implemented | 1-2 weeks | `/stride:implement` → moves here |
| **blocked/** | Paused due to dependencies/blockers | Variable | `/stride:block <ID> "reason"` |
| **review/** | Code done, awaiting testing/approval | 1-3 days | `/stride:submit <ID>` |
| **completed/** | Shipped to production | Permanent | `/stride:complete <ID>` |

### Key Benefits

- **Visual Status Tracking**: Folders immediately show sprint health
- **No Manual Archiving**: Sprints stay in `completed/` with metadata
- **Blocker Visibility**: `blocked/` folder makes impediments explicit
- **Review Stage**: Separates "code done" from "shipped"
- **Retrospectives**: Captures lessons learned in `completed/` sprints

---

## **8. Command Interface**

Stride provides two interfaces for sprint management:

### **AI Agent Commands** (In-Editor)
Slash commands used within AI agents (Claude Code, GitHub Copilot, Windsurf, etc.):

| Command | Description |
|---------|-------------|
| `/stride:init` | Initialize project context in AI agent |
| `/stride:plan <feature>` | Generate sprint plan (creates in `proposed/`) |
| `/stride:present <ID>` | Show plan with Mermaid diagrams |
| `/stride:implement <ID>` | Execute sprint implementation (moves to `active/`) |
| `/stride:feedback <ID> "note"` | Apply feedback to active sprint |
| `/stride:block <ID> "reason"` | Mark sprint as blocked |
| `/stride:unblock <ID>` | Resume blocked sprint |
| `/stride:submit <ID>` | Submit for review (moves to `review/`) |
| `/stride:complete <ID>` | Finalize and merge sprint (moves to `completed/`) |

### **CLI Commands** (Terminal)
System-level management, monitoring, and configuration:

#### Setup Commands

**`stride init`** - Initialize Stride framework in project
```bash
stride init
```
- Creates `stride/` folder structure
- Generates `AGENTS.md` with workflow instructions
- Prompts for AI agent selection (Claude Code, Copilot, Windsurf, etc.)
- Generates agent-specific configs

**`stride login`** - Authenticate user for tracking
```bash
stride login
```
- Enables sprint authorship tracking
- Associates user with project sprints
- Stores credentials in `~/.stride/config`

**`stride logout`** - Log out current user
```bash
stride logout
```

#### Monitoring Commands

**`stride status`** - Sprint distribution dashboard
```bash
stride status
stride status --user dev@example.com
stride status --detailed
```
Shows sprint counts across all status folders with team activity.

**`stride progress <ID>`** - Detailed progress for specific sprint
```bash
stride progress SPRINT-7K9P
```
Displays task completion, time estimates, and feedback history.

**`stride watch <ID>`** - Live monitoring of sprint implementation
```bash
stride watch SPRINT-7K9P --follow
```
Streams real-time updates as sprint progresses.

**`stride timeline <ID>`** - Sprint history and activity log
```bash
stride timeline SPRINT-7K9P
```
Shows chronological events (created, moved, feedback, completed).

**`stride list`** - List sprints with filtering
```bash
stride list
stride list --status active
stride list --user dev@example.com
stride list --format json
```
Filter by status, user, or export as JSON.

**`stride show <ID>`** - Display complete sprint details
```bash
stride show SPRINT-7K9P
```
Shows proposal, plan, implementation notes, and feedback log.

**`stride diff <ID>`** - Show spec deltas in sprint
```bash
stride diff SPRINT-7K9P
```
Displays changes to specs made during sprint.

#### Quality Commands

**`stride validate <ID>`** - Validate sprint structure
```bash
stride validate SPRINT-7K9P
stride validate SPRINT-7K9P --strict
```
Checks template compliance, metadata, and optional code quality (linting, tests, coverage).

#### Configuration Commands

**`stride config`** - Manage Stride configuration
```bash
stride config              # Interactive menu
stride config agents       # Add/remove AI agents
stride config show         # Display current config
stride config set <key> <value>
```
Manage AI agents, user settings, project settings, and validation rules.

#### Maintenance Commands

**`stride doctor`** - Validate installation and project health
```bash
stride doctor
stride doctor --fix
```
Checks Stride installation, project structure, configuration, and sprint health.

**`stride export`** - Export sprint data
```bash
stride export
stride export --format markdown
stride export --sprints completed
stride export --user dev@example.com
```
Generate reports (JSON, Markdown, HTML) for stakeholders or integration with project management tools.

**`stride update`** - Update Stride framework
```bash
stride update
stride update --check
```
Updates to latest version and regenerates configs.

---

## **9. Sample Workflow**

### **Initial Setup (CLI)**
```bash
# 1. Initialize Stride framework
stride init
> Select AI agents: [x] Claude Code [x] GitHub Copilot
✓ Created stride/ directory structure
✓ Configured agents

# 2. Authenticate for tracking
stride login
> Email: dev@example.com
✓ Authenticated as dev@example.com
```

### **Sprint Execution (AI Agent)**
```bash
# 3. Start a new feature (in AI agent)
/stride:init
> "Build a meme generator CLI with image overlays"

# 4. Generate sprint (creates in proposed/)
/stride:plan "Add text overlay with font support"
→ Created: sprints/proposed/SPRINT-7K9P/

# 5. Review plan
/stride:present SPRINT-7K9P
→ Mermaid task graph + risk flags

# 6. Implement (moves to active/)
/stride:implement SPRINT-7K9P
→ Moved to: sprints/active/SPRINT-7K9P/
→ Writes code, adds tests, outputs notes

# 7. Feedback (while active)
/stride:feedback SPRINT-7K9P "Use Pillow instead of Canvas"
→ Agent updates plan, re-implements
```

### **Monitoring Progress (CLI)**
```bash
# 8. Check overall status
stride status
→ Active: 2 sprints | Blocked: 1 sprint | Review: 3 sprints

# 9. Monitor specific sprint
stride progress SPRINT-7K9P
→ 67% complete | 2h remaining | Task 3 in progress

# 10. Watch live updates
stride watch SPRINT-7K9P
→ [15:20] Started Task 3: Token validation middleware
→ [15:25] Progress: 78% complete
```

### **Sprint Lifecycle (AI Agent)**
```bash
# 11. Block if needed
/stride:block SPRINT-7K9P "Waiting on font licensing approval"
→ Moved to: sprints/blocked/SPRINT-7K9P/

# 12. Unblock and continue
/stride:unblock SPRINT-7K9P
→ Moved to: sprints/active/SPRINT-7K9P/

# 13. Submit for review
/stride:submit SPRINT-7K9P
→ Moved to: sprints/review/SPRINT-7K9P/

# 14. Complete and ship
/stride:complete SPRINT-7K9P
→ Moved to: sprints/completed/SPRINT-7K9P/
→ Merged spec deltas to stride/specs/
→ Created retrospective.md
```

### **Quality & Reporting (CLI)**
```bash
# 15. Validate sprint quality
stride validate SPRINT-7K9P
→ Overall Score: 94/100 (Excellent)

# 16. View sprint history
stride timeline SPRINT-7K9P
→ Shows all events: created, moved, feedback, completed

# 17. Export for stakeholders
stride export --format markdown --sprints completed
→ Exported to reports/sprints-2025-11.md

# 18. Team analytics
stride status --team
→ Shows team activity, completed sprints, average duration
```

---

## **10. Competitive Differentiation**

| | **OpenSpec** | **SpecKit** | **Stride** |
|---|--------------|-------------|-----------|
| **Greenfield** | Good | Weak | Excellent |
| **Brownfield** | Excellent | Weak | Excellent (with Introspection) |
| **Speed** | Medium | Slow | Fast (Lite Mode) |
| **Rigor** | Medium | High | High (Validation) |
| **Feedback Loop** | Weak | Weak | Excellent (Real-time) |
| **Multi-Tool** | Excellent | Medium | Excellent (AGENTS.md) |
| **Status Tracking** | Weak | Weak | Excellent (Folder-Based + CLI) |
| **Live Monitoring** | None | None | Excellent (`stride watch`) |
| **Team Collaboration** | Weak | Medium | Excellent (User tracking) |
| **Blocker Management** | None | Weak | Explicit (blocked/ folder) |
| **Reporting** | Weak | Medium | Excellent (Export + Analytics) |
| **Audit Trail** | Excellent | High | Excellent + Timeline + Retrospectives |

**Stride = OpenSpec's portability + SpecKit's validation + Agile velocity + DevOps monitoring + Team collaboration**

### Key Differentiators

1. **Dual Interface**: AI agent commands (in-editor) + CLI commands (terminal) for complete workflow coverage
2. **Real-Time Monitoring**: `stride watch` provides live sprint progress streaming
3. **Team Analytics**: User authentication enables authorship tracking and team collaboration
4. **Visual Status Management**: Folder-based status + CLI dashboard for instant sprint health visibility
5. **Comprehensive Reporting**: Export to Markdown/HTML/JSON for stakeholder communication
6. **Health Monitoring**: `stride doctor` validates entire project setup and sprint consistency

---

## **11. MVP Success Metrics (Q1 2026)**

| Metric | Target | Measurement |
|-------|--------|-------------|
| **GitHub Stars** | 2,000+ | Community adoption |
| **Active Users** | 500+ | Weekly active CLI usage |
| **Sprint Completion Rate** | >85% | Sprints reaching `completed/` folder |
| **Feedback Loop Usage** | >60% | Sprints using `/stride:feedback` |
| **Tool Integrations** | 5+ agents | Claude Code, Copilot, Windsurf, Gemini CLI, Kilo Code |
| **Average Sprint Duration** | <5 days | Time from `proposed/` to `completed/` |
| **User Retention** | >70% | Users active after 30 days |
| **Export Usage** | >40% | Projects using `stride export` |
| **Validation Adoption** | >50% | Projects using `stride validate` |

---

## **12. Roadmap**

### **Q4 2025 - Foundation**
- ✅ Core framework design
- ✅ Status-driven folder structure
- 🔨 MVP CLI implementation (`init`, `status`, `list`, `show`)
- 🔨 AI agent command specification (`/stride:plan`, `/stride:implement`)
- 🔨 Basic validation and health checks

### **Q1 2026 - Launch**
- 🎯 Complete CLI suite (all 15 commands)
- 🎯 User authentication (`stride login`)
- 🎯 Live monitoring (`stride watch`)
- 🎯 Multi-agent support (Claude Code, Copilot, Windsurf, Gemini CLI, Kilo Code)
- 🎯 Export capabilities (Markdown, HTML, JSON)
- 🎯 VS Code extension (optional)
- 🎯 Documentation and tutorials
- 🎯 Community launch

### **Q2 2026 - Enhancement**
- 🔮 Validation pipelines (auto-lint, type-check, test coverage)
- 🔮 Introspection engine (legacy code analysis)
- 🔮 Auto-retrospectives on sprint completion
- 🔮 Blocker analytics dashboard
- 🔮 Integration APIs (Jira, Linear, GitHub Issues)
- 🔮 Stride Hub (Community sprints)
- 🔮 Team collaboration features

### **Q3 2026 - Enterprise**
- 🔮 Advanced provenance scores (spec alignment metrics)
- 🔮 Enterprise SSO and permissions
- 🔮 Custom validation rules and hooks
- 🔮 CI/CD pipeline integrations
- 🔮 Multi-project management
- 🔮 Audit and compliance features
- 🔮 Private Stride Hub for enterprises

**Legend:** ✅ Complete | 🔨 In Progress | 🎯 Next Quarter | 🔮 Future

---

## **13. Risks & Mitigations**

| Risk | Impact | Mitigation Strategy |
|------|--------|---------------------|
| **AI Hallucination** | Sprint implementation produces incorrect code | Validation pipelines + human review gates + `stride validate` |
| **Sprint Creep** | Sprints grow beyond scope | Lite Mode + auto-task caps + feedback enforcement |
| **Tool Lock-in** | Users dependent on specific AI agent | `AGENTS.md` + fallback stubs + agent-agnostic design |
| **Adoption Lag** | Slow community uptake | Co-market with Cursor, Claude, Windsurf + seed Stride Hub |
| **Complexity Overload** | Users overwhelmed by commands | Progressive disclosure +  `stride doctor` guidance |
| **Team Conflicts** | Multiple users editing same sprint | File-based locking + clear sprint ownership + conflict detection |
| **Data Loss** | Sprint data corruption | Git-tracked folders + backup recommendations + `stride doctor` checks |

---

## **14. Call to Action**

**Stride is open for contribution.**  
Let's build the future of AI-native development—**spec-driven, sprint-powered, human-aligned.**

---

## **Quick Reference**

### AI Agent Commands (In-Editor)
```bash
/stride:init                       # Initialize project context
/stride:plan "feature"             # Create sprint plan
/stride:present SPRINT-ID          # Show plan with diagrams
/stride:implement SPRINT-ID        # Execute sprint
/stride:feedback SPRINT-ID "note"  # Apply feedback
/stride:block SPRINT-ID "reason"   # Mark as blocked
/stride:unblock SPRINT-ID          # Resume sprint
/stride:submit SPRINT-ID           # Submit for review
/stride:complete SPRINT-ID         # Finalize sprint
```

### CLI Commands (Terminal)
```bash
# Setup
stride init                        # Initialize framework
stride login                       # Authenticate user
stride logout                      # Log out

# Monitoring
stride status                      # Dashboard overview
stride progress SPRINT-ID          # Sprint progress
stride watch SPRINT-ID             # Live monitoring
stride timeline SPRINT-ID          # Activity history
stride list                        # List sprints
stride show SPRINT-ID              # Sprint details
stride diff SPRINT-ID              # Spec changes

# Quality & Config
stride validate SPRINT-ID          # Validate sprint
stride config                      # Manage settings
stride doctor                      # Health check

# Maintenance
stride export                      # Export data
stride update                      # Update framework
```

### Common Workflows
```bash
# Quick start
stride init && stride login

# Monitor active sprints
stride status && stride list --status active

# Check specific sprint
stride progress SPRINT-7K9P && stride timeline SPRINT-7K9P

# Quality check before completion
stride validate SPRINT-7K9P && stride diff SPRINT-7K9P

# Generate report
stride export --format markdown --sprints completed
```

---

> **"Code is easy. Shipping is hard. Stride makes shipping inevitable."**  
> — *Stride Manifesto*
