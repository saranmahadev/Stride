# Contributing to Stride

First off, thank you for considering contributing to Stride! It's people like you that make Stride such a great tool for the AI-first development community.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Adding New AI Agents](#adding-new-ai-agents)
- [Testing Guidelines](#testing-guidelines)

---

## 📜 Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

---

## 🤝 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the [issue tracker](https://github.com/saranmahadev/Stride/issues) to avoid duplicates.

When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce**
- **Expected vs actual behavior**
- **Stride version** (`stride --version`)
- **Python version** (`python --version`)
- **Operating system**
- **AI agent** you were using (if applicable)
- **Error messages or logs**

**Example:**
```markdown
## Bug: stride init fails on Windows

**Stride version:** 1.0.0
**Python version:** 3.12.0
**OS:** Windows 11

**Steps to reproduce:**
1. Run `stride init`
2. Select Claude Code
3. Error appears

**Error message:**
[Paste error here]

**Expected:** Should create .claude directory
**Actual:** Permission denied error
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide detailed description** of the suggested enhancement
- **Explain why this enhancement would be useful**
- **List examples** of how it would be used
- **Include mockups or examples** if applicable

### Adding New AI Agent Support

Want to add support for a new AI agent? Great! See the [Adding New AI Agents](#adding-new-ai-agents) section below.

### Improving Documentation

- Fix typos, grammar, or clarity issues
- Add examples and tutorials
- Improve API documentation
- Translate documentation (future)

---

## 🛠️ Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- A GitHub account

### Step 1: Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR-USERNAME/Stride.git
cd Stride

# Add upstream remote
git remote add upstream https://github.com/saranmahadev/Stride.git
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate it
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Verify installation
stride --version
```

### Step 4: Create a Branch

```bash
# Update your fork
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

---

## 🔄 Pull Request Process

### 1. Make Your Changes

- Follow the [coding standards](#coding-standards)
- Write or update tests
- Update documentation as needed
- Keep commits atomic and well-described

### 2. Test Your Changes

```bash
# Run tests
pytest

# Check coverage
pytest --cov=stride --cov-report=html

# Run linting
black stride/
isort stride/
mypy stride/
```

### 3. Commit Your Changes

Use clear, descriptive commit messages:

```bash
# Good commit messages:
git commit -m "Add support for new AI agent: SuperCoder"
git commit -m "Fix sprint parsing when plan.md is missing"
git commit -m "Update README with installation instructions"

# Bad commit messages (avoid these):
git commit -m "fix bug"
git commit -m "updates"
git commit -m "WIP"
```

### 4. Push and Create PR

```bash
# Push to your fork
git push origin feature/your-feature-name

# Go to GitHub and create a Pull Request
```

### 5. PR Requirements

Your PR should:

- ✅ Pass all tests
- ✅ Follow coding standards (Black, isort)
- ✅ Include tests for new features
- ✅ Update documentation if needed
- ✅ Have a clear description of changes
- ✅ Reference related issues (e.g., "Fixes #123")

### 6. PR Template

When creating a PR, use this template:

```markdown
## Description
Brief description of what this PR does

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring
- [ ] Performance improvement

## Related Issues
Fixes #(issue number)

## Testing
Describe how you tested your changes

## Checklist
- [ ] Tests pass
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
```

---

## 📝 Coding Standards

### Python Style

We follow **PEP 8** with some modifications:

- **Line length**: 100 characters (configured in Black)
- **Formatter**: Black
- **Import sorting**: isort
- **Type checking**: mypy

### Code Formatting

```bash
# Format all code
black stride/

# Sort imports
isort stride/

# Type checking
mypy stride/
```

### Naming Conventions

- **Files**: `snake_case.py`
- **Classes**: `PascalCase`
- **Functions/methods**: `snake_case()`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private members**: `_leading_underscore`

### Docstrings

Use Google-style docstrings:

```python
def example_function(param1: str, param2: int) -> bool:
    """
    Brief description of what this function does.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When param2 is negative
    """
    pass
```

### File Organization

- **One command per file** in `stride/commands/`
- **Business logic** in `stride/core/`
- **Data models** in `stride/models.py`
- **Constants** in `stride/constants.py`

---

## 🤖 Adding New AI Agents

Want to add support for a new AI agent? Follow these steps:

### 1. Add Agent Configuration

Edit `stride/core/agent_registry.py`:

```python
"new-agent": AgentConfig(
    name="New Agent Name",
    key="new-agent",
    directory=".newagent/commands",
    extension=".md",
    description="Brief description",
    format_type="yaml-rich-metadata",  # Choose appropriate format
    filename_pattern="stride-{command}",
),
```

### 2. Determine Format Type

Choose from existing format types:
- `yaml-rich-metadata` (Claude, CodeBuddy, Crush, Qoder)
- `yaml-name-id` (Cursor, iFlow)
- `yaml-arguments` (Codex, Auggie, Factory)
- `yaml-xml-tags` (Amazon Q, OpenCode)
- `yaml-auto-exec` (Windsurf)
- `yaml-github-copilot` (GitHub Copilot)
- `toml` (Qwen, Gemini, Codex)
- `markdown-heading` (Cline, RooCode)
- `no-frontmatter` (KiloCode)

Or create a new format type in `stride/core/template_converter.py`.

### 3. Update Documentation

- Add agent to README.md
- Add agent to FEATURES.md
- Update agent count in documentation

### 4. Test the Agent

```bash
stride init
# Select your new agent
# Verify commands are created correctly
```

### 5. Create PR

Include:
- Agent configuration
- Test results
- Screenshots of generated commands
- Link to agent's official documentation

---

## 🧪 Testing Guidelines

### Writing Tests

Place tests in the `tests/` directory:

```
tests/
├── test_sprint_manager.py
├── test_markdown_parser.py
├── test_agent_registry.py
└── ...
```

### Test Structure

```python
import pytest
from stride.core.sprint_manager import SprintManager

def test_sprint_creation():
    """Test that sprints are created correctly."""
    manager = SprintManager()
    sprint = manager.create_sprint("Test Sprint")
    assert sprint.title == "Test Sprint"
    assert sprint.status == "proposed"
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_sprint_manager.py

# Run with coverage
pytest --cov=stride --cov-report=html

# View coverage report
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
```

---

## 📚 Documentation Guidelines

### Updating Documentation

When you make changes, update:

1. **Docstrings** in code
2. **README.md** for user-facing changes
3. **FEATURES.md** for new features
4. **CHANGELOG.md** for version changes
5. **CLAUDE.md** for development changes

### Documentation Style

- Use **clear, concise language**
- Include **code examples**
- Add **screenshots** when helpful
- Keep **formatting consistent**
- Check for **spelling and grammar**

---

## 🔍 Code Review Process

### What Reviewers Look For

- **Functionality**: Does it work as intended?
- **Tests**: Are there tests? Do they pass?
- **Code Quality**: Follows style guide?
- **Documentation**: Is it documented?
- **Breaking Changes**: Are they necessary and documented?
- **Performance**: Any performance implications?

### After Review

- **Address feedback** promptly
- **Ask questions** if feedback is unclear
- **Update PR** based on feedback
- **Be patient** - reviews take time!

---

## 🎯 First Time Contributors

Welcome! Here are some good first issues:

- 🐛 Fix typos in documentation
- 📝 Improve docstrings
- ✨ Add examples to README
- 🧪 Add tests for existing code
- 🎨 Improve error messages

Look for issues labeled [`good first issue`](https://github.com/saranmahadev/Stride/labels/good%20first%20issue).

---

## 💬 Getting Help

- **Questions?** Open a [GitHub Discussion](https://github.com/saranmahadev/Stride/discussions)
- **Bugs?** Open an [Issue](https://github.com/saranmahadev/Stride/issues)
- **Need clarification?** Comment on the relevant issue or PR

---

## 🏆 Recognition

Contributors are recognized in:
- GitHub Contributors page
- CHANGELOG.md for significant contributions
- Future Hall of Fame page (coming soon!)

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Stride! 🎉

Your efforts help make AI-first development better for everyone.
