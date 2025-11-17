# Stride Development

This directory contains the source code for the Stride framework.

## Project Structure

```
stride/
├── cli/              # CLI commands
│   ├── commands/     # Individual command implementations
│   └── main.py       # CLI entry point
├── core/             # Core framework logic
│   ├── folder_manager.py
│   ├── sprint_manager.py
│   └── config_manager.py
├── templates/        # Jinja2 templates for sprint files
├── utils/            # Utility functions
├── config/           # Default configuration
└── __init__.py       # Package initialization
```

## Development Setup

### 1. Create Virtual Environment

```powershell
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install Dependencies

```powershell
# Install in development mode
pip install -e .

# Or install with dev dependencies
pip install -e .[dev]
```

### 3. Verify Installation

```powershell
# Check if stride command is available
stride --version

# Try importing the package
python -c "import stride; print(stride.__version__)"
```

## Development Workflow

### Running Tests

```powershell
# Run all tests
pytest

# Run with coverage
pytest --cov=stride --cov-report=html

# Run specific test file
pytest tests/test_core.py
```

### Code Formatting

```powershell
# Format code with black
black stride/ tests/

# Check formatting
black --check stride/ tests/
```

### Linting

```powershell
# Run flake8
flake8 stride/ tests/

# Run mypy for type checking
mypy stride/
```

## Making Changes

1. **Create a feature branch**
   ```powershell
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow Python PEP 8 style guide
   - Add type hints to all functions
   - Write docstrings for all public functions
   - Add tests for new functionality

3. **Test your changes**
   ```powershell
   pytest
   black --check stride/ tests/
   flake8 stride/ tests/
   ```

4. **Commit and push**
   ```powershell
   git add .
   git commit -m "feat: add your feature description"
   git push origin feature/your-feature-name
   ```

## Adding New Commands

To add a new CLI command:

1. Create a new file in `stride/cli/commands/`
2. Implement the command using Click
3. Register the command in `stride/cli/main.py`

Example:

```python
# stride/cli/commands/mycommand.py
import click

@click.command()
def mycommand():
    """Description of my command."""
    click.echo("Hello from my command!")
```

```python
# stride/cli/main.py
from stride.cli.commands.mycommand import mycommand

@click.group()
def cli():
    pass

cli.add_command(mycommand)
```

## Project Guidelines

### Code Style
- Use Black for formatting (line length: 100)
- Use type hints for all function parameters and return values
- Write comprehensive docstrings using Google style

### Testing
- Maintain >80% code coverage
- Write unit tests for all core functionality
- Add integration tests for CLI commands

### Documentation
- Update README.md when adding new features
- Keep ROADMAP.md current with implementation progress
- Document breaking changes in CHANGELOG.md

## Debugging

### Enable Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Common Issues

**Import errors after installing:**
- Make sure you installed in editable mode: `pip install -e .`
- Restart your terminal/IDE

**Tests failing:**
- Ensure all dependencies are installed: `pip install -e .[dev]`
- Check Python version: `python --version` (requires 3.11+)

## Resources

- [Click Documentation](https://click.palletsprojects.com/)
- [PyYAML Documentation](https://pyyaml.org/wiki/PyYAMLDocumentation)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)
- [pytest Documentation](https://docs.pytest.org/)

## Questions?

Open an issue on GitHub or check the main README.md for more information.
