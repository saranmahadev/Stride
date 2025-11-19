"""
Template Manager for Stride AI Agent Integration

Manages templates for:
1. Root stub configs (short overview files)
2. Full workflow documentation (stride/AGENTS.md)
3. Slash command prompts (TOML and Markdown formats)
"""

from typing import Dict, Optional
from pathlib import Path


class TemplateManager:
    """Manages all templates for AI agent integration."""
    
    # The 9 Stride workflows
    WORKFLOWS = [
        'init',
        'plan',
        'present',
        'implement',
        'feedback',
        'block',
        'unblock',
        'submit',
        'complete'
    ]
    
    @classmethod
    def get_root_stub(cls, tool_name: str) -> str:
        """
        Get root stub template for a specific tool.
        
        Args:
            tool_name: Name of the AI tool
            
        Returns:
            Root stub template content
        """
        return f"""# Stride Sprint Management

This project uses **Stride** for sprint-based development with AI agents.

## Quick Command Reference

| Command | Purpose |
|---------|---------|
| `/stride:init` | Initialize project context and introspect repository |
| `/stride:plan` | Create sprint plan with tasks and estimates |
| `/stride:present` | Present sprint plan with visual diagrams |
| `/stride:implement` | Execute sprint implementation |
| `/stride:feedback` | Apply real-time corrections during sprint |
| `/stride:block` | Mark sprint as blocked due to dependencies |
| `/stride:unblock` | Resume blocked sprint |
| `/stride:submit` | Submit sprint for review and testing |
| `/stride:complete` | Finalize sprint and generate retrospective |

## Before You Start

Always run these CLI commands first to understand project state:

```bash
stride progress           # View all sprint statuses
stride info <SPRINT-ID>   # View specific sprint details
stride doctor             # Check project health
```

## Full Workflow Documentation

See **`stride/AGENTS.md`** for complete instructions on each workflow,
including context requirements, step-by-step guides, and examples.

## Project Structure

```
stride/
├── sprints/
│   ├── proposed/    # Sprint proposals awaiting approval
│   ├── active/      # Currently implementing
│   ├── blocked/     # Waiting on dependencies
│   ├── review/      # Ready for testing
│   └── completed/   # Shipped with retrospectives
└── specs/           # Living specifications
```

## Integration Notes

This file is managed by Stride. Content between STRIDE:START and STRIDE:END
markers will be updated automatically. You can add custom instructions
above or below the managed section.
"""
    
    @classmethod
    def get_full_agents_md(cls) -> str:
        """
        Get complete AGENTS.md template with all 9 workflows documented.
        
        Returns:
            Full AGENTS.md content
        """
        return """# Stride AI Agent Integration Guide

This document provides complete workflow instructions for AI agents working with Stride sprint management.

## Table of Contents

1. [Overview](#overview)
2. [Project Context](#project-context)
3. [Workflow Commands](#workflow-commands)
4. [Best Practices](#best-practices)

---

## Overview

Stride is a sprint-based development framework that manages features through time-boxed sprints with explicit state transitions.

### Sprint Lifecycle

```
proposed/ → active/ → [blocked/] → review/ → completed/
```

### The 9 Workflows

| Phase | Command | Purpose |
|-------|---------|---------|
| **Setup** | `/stride:init` | Initialize project context |
| **Planning** | `/stride:plan` | Create sprint with tasks |
| **Planning** | `/stride:present` | Review sprint plan |
| **Execution** | `/stride:implement` | Execute sprint code |
| **Execution** | `/stride:feedback` | Apply corrections |
| **Management** | `/stride:block` | Pause sprint |
| **Management** | `/stride:unblock` | Resume sprint |
| **Review** | `/stride:submit` | Submit for testing |
| **Closure** | `/stride:complete` | Finalize sprint |

---

## Project Context

### Always Check First

Before planning or implementing, run these CLI commands:

```bash
# View all sprint statuses
stride progress

# View specific sprint
stride info SPRINT-XXX

# Check project health
stride doctor

# List sprints by status
stride list --status active
stride list --status blocked
```

### Understanding Sprint State

- **proposed/**: Sprint planned but not started
- **active/**: Currently being implemented
- **blocked/**: Waiting on dependencies or decisions
- **review/**: Implementation done, awaiting verification
- **completed/**: Shipped to production with retrospective

---

## Workflow Commands

### 1. `/stride:init` - Initialize Project

**Purpose**: Set up Stride context and scan repository structure.

**When to Use**: First time working on a project, or when context is lost.

**Steps**:
1. Scan repository structure
2. Read `stride/project.md` for conventions
3. Check existing sprints with `stride progress`
4. Identify tech stack and architecture
5. Summarize project state for future commands

**Output**: Mental model of project ready for sprint planning.

---

### 2. `/stride:plan` - Create Sprint Plan

**Purpose**: Generate sprint proposal with tasks, estimates, and risks.

**When to Use**: User describes a feature to implement.

**Steps**:
1. Analyze feature requirements
2. Break into 5-10 implementable tasks
3. Estimate effort (story points: 1, 2, 3, 5, 8)
4. Identify dependencies between tasks
5. Note risks and assumptions
6. Create sprint in `proposed/` folder
7. Generate Mermaid diagram of task flow

**CLI Commands Used**:
```bash
stride plan "<sprint-name>"
stride task add <SPRINT-ID> "<task-description>"
stride task estimate <TASK-ID> <points>
```

**Output**: 
- Sprint folder in `stride/sprints/proposed/SPRINT-XXX/`
- `proposal.md` with overview
- `plan.md` with tasks and estimates
- Mermaid diagram showing task dependencies

---

### 3. `/stride:present` - Present Sprint Plan

**Purpose**: Show sprint overview with visual diagrams for review.

**When to Use**: After creating plan, before implementation.

**Steps**:
1. Read sprint from `proposed/` folder
2. Generate Mermaid task graph
3. Highlight critical path
4. Show story point breakdown
5. List risks and assumptions
6. Wait for human approval

**Output**: Visual presentation of sprint plan.

---

### 4. `/stride:implement` - Execute Sprint

**Purpose**: Move sprint to active and implement all tasks.

**When to Use**: After plan approval.

**Steps**:
1. Move sprint: `proposed/` → `active/`
2. For each task in order:
   - Implement code changes
   - Write tests
   - Update documentation
   - Mark task complete
3. Create `implementation.md` with notes
4. Track progress

**State Transition**: 
```bash
stride move <SPRINT-ID> active
```

**Output**: 
- Completed code changes
- Tests passing
- Implementation notes in sprint folder

---

### 5. `/stride:feedback` - Apply Corrections

**Purpose**: Handle mid-sprint corrections and course changes.

**When to Use**: User requests changes during implementation.

**Steps**:
1. Read feedback from user
2. Update plan if needed
3. Reimplement affected tasks
4. Log feedback in `feedback.log`
5. Continue execution

**CLI Command**:
```bash
stride feedback <SPRINT-ID> "feedback text"
```

**Output**: Updated implementation reflecting corrections.

---

### 6. `/stride:block` - Mark Sprint Blocked

**Purpose**: Explicitly pause sprint due to external blocker.

**When to Use**: Waiting on dependencies, decisions, or external factors.

**Steps**:
1. Document blocker reason
2. Move sprint: `active/` → `blocked/`
3. Log blocking event

**CLI Command**:
```bash
stride move <SPRINT-ID> blocked
```

**Output**: Sprint in `blocked/` folder with reason documented.

---

### 7. `/stride:unblock` - Resume Sprint

**Purpose**: Resume blocked sprint after blocker is resolved.

**When to Use**: External blocker has been resolved.

**Steps**:
1. Verify blocker is resolved
2. Move sprint: `blocked/` → `active/`
3. Resume implementation from last task
4. Log unblocking event

**CLI Command**:
```bash
stride move <SPRINT-ID> active
```

**Output**: Sprint back in `active/` folder, ready to continue.

---

### 8. `/stride:submit` - Submit for Review

**Purpose**: Mark implementation complete and ready for testing.

**When to Use**: All tasks complete, code is done.

**Steps**:
1. Verify all tasks complete
2. Run validation: `stride validate <SPRINT-ID>`
3. Move sprint: `active/` → `review/`
4. Wait for testing/approval

**CLI Command**:
```bash
stride move <SPRINT-ID> review
```

**Output**: Sprint in `review/` folder awaiting verification.

---

### 9. `/stride:complete` - Finalize Sprint

**Purpose**: Close sprint, merge specs, generate retrospective.

**When to Use**: Sprint tested and approved.

**Steps**:
1. Move sprint: `review/` → `completed/`
2. Merge spec deltas to `stride/specs/`
3. Generate retrospective with:
   - What went well
   - What could improve
   - Lessons learned
   - Metrics (velocity, duration)
4. Archive sprint

**CLI Command**:
```bash
stride move <SPRINT-ID> completed
```

**Output**: 
- Sprint in `completed/` folder
- `retrospective.md` generated
- Specs updated in `stride/specs/`

---

## Best Practices

### 1. Always Start with Context
- Run `/stride:init` first
- Check `stride progress` before planning
- Read existing sprints to understand conventions

### 2. Keep Sprints Small
- 5-10 tasks per sprint
- Total story points: 13-40
- Duration: 1-2 weeks max

### 3. Use Feedback Loops
- Apply `/stride:feedback` when course corrections needed
- Don't restart sprint, iterate in place

### 4. Explicit Blockers
- Use `/stride:block` immediately when stuck
- Document blocker clearly
- Use `/stride:unblock` when resolved

### 5. Quality Gates
- Run `stride validate` before `/stride:submit`
- Ensure tests pass
- Check documentation updated

### 6. Learn from Retrospectives
- Read past retrospectives before planning
- Apply lessons learned
- Track velocity trends

---

## Sprint State Reference

### Folder Structure
```
stride/sprints/
├── proposed/SPRINT-XXX/
│   ├── proposal.md
│   └── plan.md
│
├── active/SPRINT-YYY/
│   ├── proposal.md
│   ├── plan.md
│   ├── design.md
│   ├── implementation.md
│   └── feedback.log
│
├── blocked/SPRINT-ZZZ/
│   └── (same structure)
│
├── review/SPRINT-AAA/
│   └── (same structure)
│
└── completed/SPRINT-BBB/
    ├── proposal.md
    ├── plan.md
    ├── implementation.md
    └── retrospective.md
```

### CLI Quick Reference

```bash
# Setup
stride init                    # Initialize Stride
stride login                   # Authenticate

# Monitoring
stride status                  # Dashboard
stride progress <ID>           # Sprint progress
stride watch <ID>              # Live monitoring
stride timeline <ID>           # Activity history

# Quality
stride validate <ID>           # Validate sprint
stride doctor                  # Health check

# Management
stride list                    # List sprints
stride show <ID>               # Show details
stride diff <ID>               # Show changes

# Export
stride export                  # Generate reports
```

---

## Integration Notes

This file provides the complete workflow reference for all AI agents.
Individual tool configurations (CLAUDE.md, CURSOR.md, etc.) point here
for detailed instructions.

Keep this file updated as Stride workflows evolve.
"""
    
    @classmethod
    def get_slash_command_toml(cls, workflow: str) -> str:
        """
        Get TOML template for a specific workflow slash command.
        
        Args:
            workflow: One of the 9 workflow names
            
        Returns:
            TOML slash command template
        """
        # Workflow-specific details
        workflows_meta = {
            'init': {
                'description': 'Initialize Stride project context and scan repository',
                'phase': 'Setup',
                'state_transition': 'None'
            },
            'plan': {
                'description': 'Create a new sprint plan with tasks and estimates',
                'phase': 'Planning',
                'state_transition': '→ proposed/'
            },
            'present': {
                'description': 'Present sprint plan with visual diagrams',
                'phase': 'Planning',
                'state_transition': 'None'
            },
            'implement': {
                'description': 'Execute sprint implementation',
                'phase': 'Execution',
                'state_transition': 'proposed/ → active/'
            },
            'feedback': {
                'description': 'Apply real-time corrections during sprint',
                'phase': 'Execution',
                'state_transition': 'None'
            },
            'block': {
                'description': 'Mark sprint as blocked due to dependencies',
                'phase': 'Management',
                'state_transition': 'active/ → blocked/'
            },
            'unblock': {
                'description': 'Resume blocked sprint',
                'phase': 'Management',
                'state_transition': 'blocked/ → active/'
            },
            'submit': {
                'description': 'Submit sprint for review and testing',
                'phase': 'Review',
                'state_transition': 'active/ → review/'
            },
            'complete': {
                'description': 'Finalize sprint and generate retrospective',
                'phase': 'Closure',
                'state_transition': 'review/ → completed/'
            }
        }
        
        meta = workflows_meta.get(workflow, {})
        
        return f'''name = "stride-{workflow}"
description = "{meta.get('description', f'Stride {workflow} workflow')}"

# STRIDE:START
prompt = """
You are executing the Stride /{workflow} workflow.

**Phase**: {meta.get('phase', 'Unknown')}
**State Transition**: {meta.get('state_transition', 'None')}

## Context Required

Before executing this workflow, you must:

1. Read `stride/AGENTS.md` for complete workflow documentation
2. Run: `stride progress` to see all sprint statuses
3. Run: `stride doctor` to verify project health
4. Understand the current sprint state

## Workflow Steps

See `stride/AGENTS.md` section "/{workflow}" for detailed step-by-step instructions.

## Key Points

- Follow the documented workflow exactly
- Use CLI commands to update sprint state
- Log all actions in appropriate sprint files
- Preserve existing context and customizations
- Generate required outputs (Mermaid diagrams, retrospectives, etc.)

## Output Format

Your output should match the format specified in `stride/AGENTS.md`
for this workflow.

## Error Handling

If you encounter issues:
1. Check `stride doctor` for project health
2. Verify sprint exists and is in correct state
3. Review `stride/AGENTS.md` for workflow requirements
4. Ask user for clarification if needed

Always refer to `stride/AGENTS.md` as the source of truth.
"""
# STRIDE:END
'''
    
    @classmethod
    def get_slash_command_markdown(cls, workflow: str) -> str:
        """
        Get Markdown template for a specific workflow (Windsurf/Antigravity format).
        
        Args:
            workflow: One of the 9 workflow names
            
        Returns:
            Markdown workflow template
        """
        workflows_meta = {
            'init': {
                'description': 'Initialize Stride project context and scan repository',
                'auto_execution': 3
            },
            'plan': {
                'description': 'Create a new sprint plan with tasks and estimates',
                'auto_execution': 2
            },
            'present': {
                'description': 'Present sprint plan with visual diagrams',
                'auto_execution': 3
            },
            'implement': {
                'description': 'Execute sprint implementation',
                'auto_execution': 1
            },
            'feedback': {
                'description': 'Apply real-time corrections during sprint',
                'auto_execution': 2
            },
            'block': {
                'description': 'Mark sprint as blocked due to dependencies',
                'auto_execution': 3
            },
            'unblock': {
                'description': 'Resume blocked sprint',
                'auto_execution': 3
            },
            'submit': {
                'description': 'Submit sprint for review and testing',
                'auto_execution': 2
            },
            'complete': {
                'description': 'Finalize sprint and generate retrospective',
                'auto_execution': 1
            }
        }
        
        meta = workflows_meta.get(workflow, {})
        
        return f'''---
description: {meta.get('description', f'Stride {workflow} workflow')}
auto_execution_mode: {meta.get('auto_execution', 2)}
---

<!-- STRIDE:START -->

# Stride /{workflow} Workflow

You are executing the **Stride {workflow}** workflow.

## Pre-Flight Checks

Before starting, verify:

```bash
stride progress    # Check sprint statuses
stride doctor      # Verify project health
```

## Workflow Documentation

Refer to `stride/AGENTS.md` for complete step-by-step instructions
for the `/{workflow}` workflow.

## Execution Steps

1. **Read Full Documentation**: Open `stride/AGENTS.md` and read the 
   section for `/{workflow}`

2. **Understand Context**: Check which sprint folder is relevant:
   - `proposed/` - Planning phase
   - `active/` - Execution phase
   - `blocked/` - Waiting on blockers
   - `review/` - Testing phase
   - `completed/` - Done

3. **Follow Steps**: Execute each step from `stride/AGENTS.md` exactly

4. **Update State**: Use CLI commands to update sprint state:
   ```bash
   stride move <SPRINT-ID> <new-status>
   ```

5. **Generate Outputs**: Create required files (plans, implementations,
   retrospectives, etc.)

## Key Reminders

- ✅ Always start with context (run CLI commands first)
- ✅ Follow documented workflow from `stride/AGENTS.md`
- ✅ Use CLI commands to update sprint state
- ✅ Log actions in sprint files
- ✅ Generate required outputs (diagrams, notes, etc.)

## Need Help?

- Check `stride/AGENTS.md` for workflow details
- Run `stride doctor` for project health
- Run `stride show <SPRINT-ID>` for sprint details

<!-- STRIDE:END -->
'''
    
    @classmethod
    def get_all_slash_commands_toml(cls) -> Dict[str, str]:
        """Get all 9 workflow TOML templates."""
        return {
            workflow: cls.get_slash_command_toml(workflow)
            for workflow in cls.WORKFLOWS
        }
    
    @classmethod
    def get_all_slash_commands_markdown(cls) -> Dict[str, str]:
        """Get all 9 workflow Markdown templates."""
        return {
            workflow: cls.get_slash_command_markdown(workflow)
            for workflow in cls.WORKFLOWS
        }
