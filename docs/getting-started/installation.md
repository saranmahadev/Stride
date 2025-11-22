# Installation

This guide covers installing Stride on various platforms.

## System Requirements

- **Python**: 3.11 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: 100MB+ free space
- **Network**: Internet access for initial download

## Installation Methods

=== "From Source (Recommended)"

    ```bash
    # Clone the repository
    git clone https://github.com/saranmahadev/Stride.git
    cd Stride

    # Create virtual environment
    python -m venv venv
    
    # Activate virtual environment
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate

    # Install dependencies
    pip install -r requirements.txt

    # Install Stride in development mode
    pip install -e .

    # Verify installation
    stride --version
    ```

=== "From PyPI (Coming Soon)"

    ```bash
    # Install from PyPI
    pip install stride-ai

    # Verify installation
    stride --version
    ```

=== "Using pipx (Isolated)"

    ```bash
    # Install pipx if not already installed
    python -m pip install --user pipx
    python -m pipx ensurepath

    # Install Stride
    pipx install stride-ai

    # Verify installation
    stride --version
    ```

## Platform-Specific Instructions

### Windows

!!! tip "Windows Users"
    Use PowerShell or Windows Terminal for the best experience.

```powershell
# Install Python from python.org if not installed
# Then follow the "From Source" instructions above

# Optional: Add to PATH
$env:PATH += ";$PWD\venv\Scripts"
```

### macOS

```bash
# Ensure Python 3.11+ is installed
python3 --version

# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.11+
brew install python@3.11

# Follow "From Source" instructions above
```

### Linux

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip

# Fedora/RHEL
sudo dnf install python3.11 python3-pip

# Follow "From Source" instructions above
```

## Verifying Installation

After installation, verify everything works:

```bash
# Check version
stride --version
# Output: Stride version 1.0.0

# Check help
stride --help
# Should show all available commands

# Run health check
stride doctor
# Should show "Installation: ✓ Stride is properly installed"
```

## Optional Dependencies

### For Development

```bash
pip install -r requirements.txt
pip install pytest pytest-cov black mypy flake8
```

### For Documentation

```bash
pip install mkdocs mkdocs-material
```

## Troubleshooting

### Python Version Issues

!!! warning "Python 3.11+ Required"
    Stride requires Python 3.11 or higher.

```bash
# Check your Python version
python --version

# If too old, install newer version
# Windows: Download from python.org
# macOS: brew install python@3.11
# Linux: Use your package manager
```

### Permission Errors

```bash
# If you get permission errors on Linux/macOS
sudo pip install -r requirements.txt

# Or use virtual environment (recommended)
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Import Errors

```bash
# If you get "Module not found" errors
pip install -r requirements.txt --force-reinstall

# Or reinstall Stride
pip install -e . --force-reinstall
```

### Command Not Found

```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

# Or add to PATH
export PATH="$PATH:$(pwd)/venv/bin"  # macOS/Linux
$env:PATH += ";$PWD\venv\Scripts"  # Windows PowerShell
```

## Updating Stride

### From Source

```bash
cd Stride
git pull origin main
pip install -r requirements.txt
pip install -e . --upgrade
```

### From PyPI (Future)

```bash
pip install --upgrade stride-ai
```

## Uninstalling

```bash
# If installed with pip
pip uninstall stride-ai

# Remove virtual environment
rm -rf venv  # macOS/Linux
Remove-Item -Recurse venv  # Windows

# Remove cloned repository
cd ..
rm -rf Stride  # macOS/Linux
Remove-Item -Recurse Stride  # Windows
```

## Next Steps

Installation complete! Now:

1. [Quick Start Guide](quickstart.md) - Create your first sprint
2. [Core Concepts](concepts.md) - Understand how Stride works
3. [User Guide](../user-guide/index.md) - Explore all features

---

Having trouble? Check our [FAQ](../about/faq.md) or [open an issue](https://github.com/saranmahadev/Stride/issues).
