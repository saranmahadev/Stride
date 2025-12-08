# Stride: 

**Stride** is an Agent-First Framework for Sprint-Powered, Spec-Driven Development. It enables AI coding agents (Claude, Cursor, Windsurf, etc.) to autonomously plan, implement, and document software features while humans monitor progress and provide strategic guidance.

### The Problem Stride Solves

**Traditional AI Coding Challenges:**
- 🔴 Context loss after 3-5 chat turns
- 🔴 No methodology or structure
- 🔴 Can't track what AI actually implemented
- 🔴 Multiple agents produce inconsistent outputs
- 🔴 No retrospectives or learnings captured

**Stride's Solution:**
- ✅ **Sprint-based structure** → Persistent context in files
- ✅ **Slash commands** → Clear workflows for agents
- ✅ **Status folders** → Visual workflow states
- ✅ **Multi-agent support** → 20 tools, unified methodology
- ✅ **Auto-retrospectives** → Learnings captured automatically
- ✅ **CLI monitoring** → Real-time visibility for humans

### Key Value Propositions

| User Type | Pain Point | Stride Solution |
|-----------|------------|-----------------|
| **Indie Hacker** | "AI writes code but I lose context in 3 chats" | `/stride:init` → sprint → ship in one flow |
| **Startup CTO** | "We use Cursor + Claude, outputs don't align" | `AGENTS.md` + `/stride:plan` → unified tasks |
| **Enterprise Dev** | "Can't trust AI in legacy repos" | `/stride:init` analyzes repo → validation pipelines |
| **AI-First Developer** | "Need to track what agents implemented" | Sprint history + validation + exports |

---

## Core Concept

### The Stride Philosophy

Stride is built on three fundamental principles:

#### 1. Agent-First Design

**AI agents do the work, humans provide direction:**

#### 2. Sprint-Based Methodology

**Every feature/bug fix/change is a sprint and each sprint has the following phases:**
- **Proposed** → Planning phase (objectives, tasks, design)
- **Active** → Implementation phase (coding, testing, notes)
- **Review** → Quality check (testing, validation)
- **Completed** → Done (retrospective, archived)

**Physical folders represent states:**
```
stride/
    sprints/
        SPRINT-AAAAA/Spec.md
        SPRINT-BBBBB/
    project.md
```

#### 3. Spec-Driven Development

**Everything documented in the markdown:**
Each Sprint
- `proposal.md` → What and why
- `plan.md` → How (tasks, approach, risks)
- `design.md` → Architecture (diagrams, APIs)
- `implementation.md` → Real-time notes and decisions
- `retrospective.md` → What worked, what didn't

**Benefits:**
- Version control tracks everything
- Both agents and humans read same files
- No hidden state in databases
- Easy to backup, restore, audit

---

### CLI Commands

stride init → To initialize stride in the folder 
stride list → See all sprints 
stride status → Check sprint state 
stride show → View sprint files 
stride validate → Check quality of sprint documents