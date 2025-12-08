# PyPI Publishing Guide for Stride (stridekit)

This guide will walk you through publishing Stride to PyPI as **stridekit**.

## 📋 Pre-Publishing Checklist

Before publishing, ensure:

- ✅ Package name: `stridekit` (set in pyproject.toml)
- ✅ Version: `1.0.0`
- ✅ LICENSE file exists
- ✅ README.md exists with banner
- ✅ All tests pass
- ✅ Code is clean and formatted
- ✅ Documentation is complete

---

## 🔧 Step 1: Install Build Tools

```bash
# Install/upgrade build tools
pip install --upgrade pip
pip install --upgrade build twine
```

**What these do:**
- `build` - Creates distribution packages (wheel and sdist)
- `twine` - Securely uploads packages to PyPI

---

## 🏗️ Step 2: Build the Package

```bash
# Navigate to project root
cd "f:\Stride Tool"

# Clean previous builds (if any)
rm -rf dist/ build/ *.egg-info

# Build the package
python -m build
```

**Expected output:**
```
Successfully built stridekit-1.0.0.tar.gz and stridekit-1.0.0-py3-none-any.whl
```

**What this creates:**
- `dist/stridekit-1.0.0-py3-none-any.whl` - Wheel distribution
- `dist/stridekit-1.0.0.tar.gz` - Source distribution

---

## 🧪 Step 3: Test on Test PyPI (IMPORTANT!)

Always test on Test PyPI first!

### 3.1: Create Test PyPI Account

1. Go to https://test.pypi.org/account/register/
2. Create an account
3. Verify your email

### 3.2: Create API Token (Test PyPI)

1. Go to https://test.pypi.org/manage/account/#api-tokens
2. Click "Add API token"
3. Token name: `stridekit-upload`
4. Scope: "Entire account" (for first upload)
5. Copy the token (starts with `pypi-`)
6. **Save it securely!** You won't see it again

### 3.3: Configure Test PyPI Credentials

Create/edit `~/.pypirc` file:

**On Windows:**
```
C:\Users\YOUR_USERNAME\.pypirc
```

**On macOS/Linux:**
```
~/.pypirc
```

**File contents:**
```ini
[testpypi]
  username = __token__
  password = pypi-YOUR_TEST_PYPI_TOKEN_HERE
```

### 3.4: Upload to Test PyPI

```bash
# Upload to Test PyPI
python -m twine upload --repository testpypi dist/*
```

**Expected output:**
```
Uploading distributions to https://test.pypi.org/legacy/
Uploading stridekit-1.0.0-py3-none-any.whl
Uploading stridekit-1.0.0.tar.gz
View at: https://test.pypi.org/project/stridekit/1.0.0/
```

### 3.5: Test Install from Test PyPI

```bash
# Create fresh test environment
python -m venv test_env
# Activate it (Windows)
test_env\Scripts\activate
# Or macOS/Linux:
source test_env/bin/activate

# Install from Test PyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ stridekit

# Test it works
stride --version
stride --help

# Try initializing
cd /tmp
mkdir test_stride
cd test_stride
stride init

# Deactivate and clean up
deactivate
cd ..
rm -rf test_stride test_env
```

**Note:** The `--extra-index-url https://pypi.org/simple/` is needed because dependencies (typer, rich, etc.) are on the real PyPI, not Test PyPI.

---

## 🚀 Step 4: Publish to Real PyPI

Once testing is successful on Test PyPI:

### 4.1: Create PyPI Account

1. Go to https://pypi.org/account/register/
2. Create an account (can use same email as Test PyPI)
3. Verify your email

### 4.2: Create API Token (Real PyPI)

1. Go to https://pypi.org/manage/account/#api-tokens
2. Click "Add API token"
3. Token name: `stridekit-upload`
4. Scope: "Entire account" (for first upload)
5. Copy the token
6. **Save it securely!**

### 4.3: Update ~/.pypirc

Add PyPI configuration to `~/.pypirc`:

```ini
[pypi]
  username = __token__
  password = pypi-YOUR_REAL_PYPI_TOKEN_HERE

[testpypi]
  username = __token__
  password = pypi-YOUR_TEST_PYPI_TOKEN_HERE
```

### 4.4: Upload to PyPI

```bash
# Upload to real PyPI
python -m twine upload dist/*
```

**Expected output:**
```
Uploading distributions to https://upload.pypi.org/legacy/
Uploading stridekit-1.0.0-py3-none-any.whl
Uploading stridekit-1.0.0.tar.gz
View at: https://pypi.org/project/stridekit/1.0.0/
```

### 4.5: Verify Installation

```bash
# Install from real PyPI
pip install stridekit

# Verify
stride --version
# Should output: 1.0.0

stride --help
# Should show all commands
```

**🎉 Congratulations! Your package is now live on PyPI!**

---

## 📊 Step 5: Post-Publishing Tasks

### 5.1: Update GitHub Release

1. Go to https://github.com/saranmahadev/Stride/releases
2. Click "Create a new release"
3. Tag: `v1.0.0`
4. Title: `Stride v1.0.0 - Initial Release`
5. Description: Copy from CHANGELOG.md
6. Publish release

### 5.2: Update README Badges

The PyPI badge in README.md should now work:
```markdown
[![PyPI version](https://img.shields.io/pypi/v/stridekit.svg)](https://pypi.org/project/stridekit/)
```

### 5.3: Announce

- Post on Twitter/X
- Share on LinkedIn
- Post on Reddit (r/Python, r/MachineLearning)
- Share in developer communities

### 5.4: Monitor

- Check https://pypi.org/project/stridekit/ for issues
- Monitor GitHub issues
- Watch download statistics

---

## 🔄 Step 6: Future Updates

### For Version Updates (e.g., 1.0.1, 1.1.0):

1. **Update version** in `stride/__init__.py`:
   ```python
   __version__ = "1.0.1"
   ```

2. **Update version** in `pyproject.toml`:
   ```toml
   version = "1.0.1"
   ```

3. **Update CHANGELOG.md** with new changes

4. **Commit changes**:
   ```bash
   git add .
   git commit -m "Release v1.0.1"
   git tag v1.0.1
   git push origin main --tags
   ```

5. **Build new package**:
   ```bash
   rm -rf dist/ build/ *.egg-info
   python -m build
   ```

6. **Test on Test PyPI** (optional but recommended):
   ```bash
   python -m twine upload --repository testpypi dist/*
   ```

7. **Upload to PyPI**:
   ```bash
   python -m twine upload dist/*
   ```

8. **Create GitHub release** for the new version

---

## 🐛 Troubleshooting

### Error: "File already exists"

**Problem:** Version already exists on PyPI
**Solution:** You cannot replace versions. Increment version number:
- Bug fix: 1.0.0 → 1.0.1
- Minor update: 1.0.0 → 1.1.0
- Major update: 1.0.0 → 2.0.0

### Error: "Invalid or non-existent authentication"

**Problem:** Wrong API token or not configured
**Solution:**
1. Regenerate API token on PyPI
2. Update `~/.pypirc` with new token
3. Make sure format is correct (username = `__token__`)

### Error: "Package name taken"

**Problem:** `stridekit` already taken (unlikely, but possible)
**Solution:**
1. Choose alternative name (e.g., `stride-cli`, `stride-tool`)
2. Update `name` in `pyproject.toml`
3. Rebuild and upload

### Templates Not Included

**Problem:** Templates not in package
**Solution:** Check `pyproject.toml` has:
```toml
[tool.setuptools.package-data]
stride = ["templates/**/*.md"]
```

### Missing Dependencies

**Problem:** Package installs but crashes
**Solution:** Check all dependencies are in `pyproject.toml`:
```toml
dependencies = [
    "typer[all]>=0.9.0",
    "rich>=13.0.0",
    ...
]
```

---

## 📝 Important Notes

### Semantic Versioning

Follow [SemVer](https://semver.org/):
- **MAJOR** (X.0.0): Breaking changes
- **MINOR** (1.X.0): New features, backward compatible
- **PATCH** (1.0.X): Bug fixes, backward compatible

### Security

- **Never commit** API tokens to Git
- **Use environment variables** for tokens in CI/CD
- **Regenerate tokens** if exposed
- **Use project-scoped tokens** after first upload

### Package Size

- Current package: ~50-100KB (code + templates)
- Keep it lightweight
- Don't include unnecessary files
- Use `.gitignore` and `MANIFEST.in` if needed

### Testing

Before each release:
```bash
# Run full test suite
pytest

# Check code quality
black stride/
isort stride/
mypy stride/

# Build and test install
python -m build
pip install dist/*.whl
stride --help
```

---

## 📚 Resources

- **PyPI Help**: https://pypi.org/help/
- **Packaging Guide**: https://packaging.python.org/
- **Twine Docs**: https://twine.readthedocs.io/
- **Setuptools**: https://setuptools.pypa.io/

---

## ✅ Quick Reference Commands

```bash
# Build
python -m build

# Test PyPI upload
python -m twine upload --repository testpypi dist/*

# Real PyPI upload
python -m twine upload dist/*

# Test install from Test PyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ stridekit

# Test install from real PyPI
pip install stridekit

# Check what's in the package
tar -tzf dist/stridekit-1.0.0.tar.gz

# Or for wheel:
unzip -l dist/stridekit-1.0.0-py3-none-any.whl
```

---

## 🎯 Success Criteria

You'll know publishing was successful when:

1. ✅ https://pypi.org/project/stridekit/ shows your package
2. ✅ `pip install stridekit` works from anywhere
3. ✅ `stride --version` shows correct version
4. ✅ `stride init` creates proper directory structure
5. ✅ All CLI commands work correctly
6. ✅ Templates are included and accessible

---

Good luck with your first PyPI publication! 🚀

If you run into issues, check:
- GitHub Issues: https://github.com/saranmahadev/Stride/issues
- PyPI Support: https://pypi.org/help/
