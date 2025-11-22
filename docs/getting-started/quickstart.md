# Quick Start

Get up and running with Stride in 5 minutes! This guide will walk you through creating your first sprint.

## Prerequisites

Make sure you've [installed Stride](installation.md) first.

## Step 1: Initialize Your Project

Navigate to your project directory and initialize Stride:

```bash
cd your-project
stride init
```

You'll see output like:

```
✓ Created stride/ directory structure
✓ Created stride/sprints/ folders
✓ Created stride/specs/ folder
✓ Created stride/project.md
✓ Stride initialized successfully!
```

## Step 2: Configure AI Agents (Optional)

If you're using AI coding assistants like Claude or Cursor:

```bash
stride agent init
```

Select your AI tools:

```
? Select AI agents to configure:
  [x] Claude Code
  [x] Cursor  
  [ ] Windsurf
  [ ] GitHub Copilot
  
✓ Configured 2 agents
✓ Created CLAUDE.md
✓ Created CURSOR.md
```

## Step 3: Authenticate (Optional)

Track your work with user authentication:

```bash
stride login
```

Enter your details:

```
? Name: Your Name
? Email: you@example.com

✓ Authenticated as you@example.com
```

## Step 4: Create Your First Sprint

Create a sprint for a new feature:

```bash
stride create \
  --title "Add dark mode toggle" \
  --description "Implement a dark mode theme switcher" \
  --priority high
```

Output:

```
✓ Created sprint: SPRINT-A1B2
✓ Location: stride/sprints/proposed/SPRINT-A1B2/
✓ Files created:
  - proposal.md

Next steps:
  stride show SPRINT-A1B2           # View sprint details
  stride move SPRINT-A1B2 active    # Start working
```

## Step 5: View Sprint Details

Check what was created:

```bash
stride show SPRINT-A1B2
```

You'll see:

```
╭─ Sprint: SPRINT-A1B2 ──────────────────────╮
│                                             │
│ Title:    Add dark mode toggle             │
│ Status:   proposed                          │
│ Priority: high                              │
│ Created:  2025-11-22 10:30:00 UTC          │
│ Author:   you@example.com                   │
│                                             │
│ Description:                                │
│ Implement a dark mode theme switcher       │
│                                             │
╰─────────────────────────────────────────────╯

Available files:
  📄 proposal.md
```

## Step 6: Move to Active

Start working on the sprint:

```bash
stride move SPRINT-A1B2 active
```

Output:

```
✓ Moved SPRINT-A1B2: proposed → active
✓ Location: stride/sprints/active/SPRINT-A1B2/
```

## Step 7: Monitor Progress

Watch your sprint in real-time:

```bash
stride watch SPRINT-A1B2
```

Or check status:

```bash
stride status SPRINT-A1B2
stride progress SPRINT-A1B2
stride timeline SPRINT-A1B2
```

## Step 8: Validate Quality

Before completing, validate your work:

```bash
stride validate SPRINT-A1B2
```

Output:

```
✓ Validating SPRINT-A1B2...

Structure:
  ✓ Sprint folder exists
  ✓ Required files present
  ✓ Metadata valid

Quality:
  ✓ Title is descriptive
  ✓ Description is clear
  ✓ Proper formatting

Overall Score: 95/100 (Excellent)
```

## Step 9: Complete the Sprint

Move to completed:

```bash
stride move SPRINT-A1B2 completed
```

Output:

```
✓ Moved SPRINT-A1B2: active → completed
✓ Location: stride/sprints/completed/SPRINT-A1B2/
✓ Sprint completed successfully!
```

## Bonus: Export Report

Generate a report of your work:

```bash
stride export --format markdown --output report.md
```

Output:

```
✓ Exported 1 sprint(s) to report.md

Summary:
  Total sprints: 1
  Completed: 1
  Format: markdown
```

## Next Steps

Congratulations! You've completed your first Stride sprint. 🎉

Now explore:

- 📖 [Core Concepts](concepts.md) - Understand the workflow
- 🤖 [AI Agents](../ai-agents/overview.md) - Integrate with AI tools
- 📚 [User Guide](../user-guide/index.md) - Learn all commands
- 🎓 [Tutorials](../tutorials/index.md) - Real-world examples

## Common Commands Cheat Sheet

```bash
# Sprint Management
stride create --title "Feature"     # Create sprint
stride list                          # List all sprints
stride show SPRINT-ID                # View details
stride move SPRINT-ID <status>       # Change status

# Monitoring
stride status SPRINT-ID              # Check status
stride progress SPRINT-ID            # View progress
stride watch SPRINT-ID               # Live monitor
stride timeline SPRINT-ID            # See history

# Quality & Reports
stride validate SPRINT-ID            # Check quality
stride doctor                        # Health check
stride export                        # Generate report

# Configuration
stride agent init                    # Setup AI agents
stride config get user.name          # Get config value
stride login                         # Authenticate
```

## Tips for Success

!!! tip "Best Practices"
    - Create sprints for discrete features
    - Move through statuses methodically
    - Validate before completing
    - Export reports regularly
    - Use descriptive titles

!!! warning "Common Mistakes"
    - Creating sprints that are too large
    - Skipping validation steps
    - Not using status folders properly
    - Forgetting to authenticate

## Getting Help

Stuck? Here's where to get help:

- 📖 [User Guide](../user-guide/index.md) - Complete reference
- ❓ [FAQ](../about/faq.md) - Common questions
- 💬 [GitHub Discussions](https://github.com/saranmahadev/Stride/discussions) - Community help
- 🐛 [Report Issues](https://github.com/saranmahadev/Stride/issues) - Found a bug?

---

Ready to dive deeper? Continue to [Core Concepts](concepts.md) →
