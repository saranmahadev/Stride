## 🔄 Development Workflow

This project follows a **talk → plan → confirm → implement** cycle:

### 1. **Talk Phase** (Discussion)
- Human explains what they want to build/change
- AI asks clarifying questions
- Explore requirements, edge cases, dependencies
- No code is written yet

### 2. **Plan Phase** (Design)
- AI creates a detailed implementation plan
- Plan includes:
  - What files will be created/modified
  - What each change will accomplish
  - Technical approach and alternatives
  - Testing strategy
  - File structure diagrams
- Plan is presented in markdown format
- **IMPORTANT**: Plan must be comprehensive and detailed

### 3. **Confirm Phase** (Approval)
- Human reviews the plan
- Human confirms: "Proceed" or requests changes
- **NO IMPLEMENTATION HAPPENS UNTIL CONFIRMATION**
- If changes needed, return to Plan phase

### 4. **Implement Phase** (Execution)
- AI executes the approved plan exactly as specified
- Makes all specified changes
- Runs tests if applicable
- Reports completion with summary

### Example Workflow

```
Human: "Add a --verbose flag to stride list"

AI: [TALK] "Should verbose mode:
       - Show full file paths?
       - Include timestamps?
       - Show descriptions?"

Human: [CONFIRM] "Show paths and timestamps"

AI: [PLAN] "Implementation Plan:
       1. Edit stride/commands/list.py
       2. Add --verbose flag using Typer
       3. Update output formatting with Rich
       4. Add tests"

Human: [APPROVAL] "Proceed"

AI: [IMPLEMENT] Executes all changes, runs tests, reports completion
```

---

## 📝 Guidelines for AI Agents

### When Working on Stride:

1. **Always follow the talk → plan → confirm → implement workflow**
2. **Never skip the planning phase** - users need to review before changes
3. **Wait for explicit confirmation** before implementing
4. **Make comprehensive plans** - include all affected files
5. **Document decisions** in implementation notes
6. **Run tests after changes** when applicable
7. **Provide clear summaries** of what was done

### Command Implementation Pattern:

```python
# stride/commands/example.py
import typer
from rich.console import Console

console = Console()

def example_command(
    arg: str,
    option: bool = False
):
    """
    Brief description of what this command does.

    Args:
        arg: Description of argument
        option: Description of option
    """
    # Implementation here
    console.print("[green]Success![/green]")
```

### File Organization Rules:

- **One command per file** in `stride/commands/`
- **Business logic** in `stride/core/`
- **Data models** in `stride/models.py`
- **Constants** in `stride/constants.py`
