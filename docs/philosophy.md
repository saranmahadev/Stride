# Philosophy

The core principles behind Stride's design.

---

## Three Pillars

Stride is built on three fundamental principles:

### 1. Agent-First Design

**AI agents do the work, humans provide direction**

- Agents use slash commands to plan, implement, and document
- Humans monitor via CLI and provide strategic guidance
- Markdown files serve as shared context between agents and humans

**Why it matters:**

- Agents are better at repetitive tasks
- Humans are better at strategic decisions
- Clear division of responsibilities

### 2. Sprint-Based Methodology

**Every feature, bug fix, or change is a sprint**

- **Proposed** → Planning phase (objectives, tasks, design)
- **Active** → Implementation phase (coding, testing, logging)
- **Completed** → Done (retrospective, learnings)

**Why it matters:**

- Forces planning before coding
- Provides structure to chaotic AI sessions
- Creates natural checkpoints

### 3. Spec-Driven Development

**Everything documented in markdown**

Each sprint contains:

- `proposal.md` → What and why
- `plan.md` → How (strides, tasks, approach)
- `design.md` → Architecture
- `implementation.md` → Real-time development log
- `retrospective.md` → Learnings

**Why it matters:**

- Version control tracks everything
- Both agents and humans read same files
- No hidden state in databases
- Easy to backup, restore, and audit

---

## Core Beliefs

### Context is Everything

**Problem:** AI loses context after 3-5 chat turns

**Solution:** Persistent context in files

```
.stride/sprints/SPRINT-XXXXX/
  ├── proposal.md       ← Context never lost
  ├── plan.md           ← Always available
  ├── implementation.md ← Builds over time
  └── retrospective.md  ← Captures learnings
```

### Process Over Tools

**Problem:** Different AI tools produce inconsistent outputs

**Solution:** Unified methodology across all agents

- All 20 agents follow same workflow
- Same file structure
- Same command names
- Consistent documentation

### Transparency and Trust

**Problem:** Can't trust what AI implemented

**Solution:** Complete audit trail

Every change logged:

- Why it was made (proposal)
- How it was planned (plan)
- When it was implemented (implementation log)
- What was learned (retrospective)

### Continuous Improvement

**Problem:** Same mistakes repeated across sprints

**Solution:** Built-in retrospectives

Every sprint ends with:

- What worked well
- What could be improved
- Key learnings
- Action items

---

## Design Decisions

### Why Markdown?

**Alternatives considered:** JSON, YAML, databases

**Why markdown won:**

- ✅ Human-readable
- ✅ AI-friendly
- ✅ Version control native
- ✅ Easy to edit manually
- ✅ No parsing complexity
- ✅ Works offline

### Why File-Based State?

**Alternatives considered:** Database, in-memory state

**Why files won:**

- ✅ No database setup
- ✅ Git tracks changes
- ✅ Visible in file explorer
- ✅ Easy backup/restore
- ✅ Platform independent
- ✅ No server needed

### Why Strides?

**Alternatives considered:** Flat task list, phases

**Why strides won:**

- ✅ Natural milestones
- ✅ Bite-sized chunks
- ✅ Clear progress indicators
- ✅ Easy to parallelize
- ✅ Logical grouping

---

## Anti-Patterns We Avoid

### ❌ Hidden State

**We don't:** Store state in databases, config files, or memory

**We do:** Everything visible in markdown files

### ❌ Tool Lock-In

**We don't:** Depend on specific AI tool

**We do:** Support 20 agents with same workflow

### ❌ Over-Engineering

**We don't:** Complex abstractions, frameworks

**We do:** Simple files, clear structure

### ❌ Magic

**We don't:** Auto-generate without human approval

**We do:** Agent proposes, human approves

---

## Inspiration

Stride draws inspiration from:

### Agile/Scrum

- Sprint-based iterations
- Retrospectives
- Incremental delivery

### Documentation-Driven Development

- Spec before code
- Design documents
- Clear requirements

### Test-Driven Development

- Define success criteria first
- Validate before completion
- Continuous validation

### DevOps

- Everything as code (docs as code)
- Version control everything
- Automation with human oversight

---

## Who Stride is For

### ✅ Indie Hackers

- Ship features fast
- Keep context across sessions
- Solo development

### ✅ Startup CTOs

- Multiple AI tools
- Consistent process
- Team alignment

### ✅ Enterprise Developers

- Audit trails
- Process compliance
- Risk management

### ✅ AI-First Developers

- Maximize AI productivity
- Maintain control
- Track everything

---

## Who Stride is NOT For

### ❌ Non-AI Workflows

If you don't use AI coding assistants, Stride adds overhead.

### ❌ Ad-Hoc Scripting

For quick one-off scripts, Stride is too much structure.

### ❌ Fully Manual Development

If you prefer writing everything yourself, Stride won't help.

---

## Future Vision

### Where We're Going

- **More Agents**: Support emerging AI tools
- **Better Analytics**: Deeper insights from sprint data
- **Team Features**: Multi-developer coordination
- **Templates**: Industry-specific sprint templates
- **Integrations**: Jira, Linear, GitHub Issues

### What Won't Change

- **File-based approach**
- **Markdown format**
- **Agent-first philosophy**
- **Sprint methodology**
- **Transparency**

---

## Quotes That Guide Us

> "Make it work, make it right, make it fast - in that order."
> — Kent Beck

> "Weeks of coding can save you hours of planning."
> — Unknown

> "The best way to predict the future is to document it."
> — Adapted from Alan Kay

---

## Next Steps

- [Features →](features.md) - See how philosophy translates to features
- [Sprint Lifecycle →](sprint-lifecycle.md) - See philosophy in action
