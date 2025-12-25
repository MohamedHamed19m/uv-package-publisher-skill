---
name: python-package-publishing
description: Streamlined workflow for packaging and distributing Python projects using UV. Use this skill when initializing new libraries, configuring CLI entry points in pyproject.toml, or building and uploading artifacts to PyPI/TestPyPI. Ideal for converting local scripts into installable tools or setting up MCP servers for distribution.

keywords: ["uv build", "pypi publishing", "pyproject.toml", "python packaging", "testpypi", "uv init", "uv publish"]
---

# Python Package Publishing with UV

This skill provides guidance for creating, building, and publishing Python packages using modern UV tooling.

## When to Use This Skill

- Packaging Python projects for distribution
- Creating CLI commands with entry points
- Publishing packages to PyPI/TestPyPI
- Setting up MCP servers as installable packages
- Converting existing Python projects into distributable packages
- Troubleshooting package installation and import issues

## Environment Reconnaissance (First Step)

Before starting, gather critical environment information:

**Check UV Installation:**
````bash
uv --version  # Verify UV is installed
````

**Check Python Version:**
````bash
python --version  # Ensure >= 3.11 for modern packaging
````

**Identify Project Type:**
- Existing codebase vs. new project
- MCP server, CLI tool, library, or application
- Dependencies and their availability on PyPI

## Approach Selection

### Decision Framework

| Condition | Recommended Approach |
|-----------|---------------------|
| New project from scratch | Use `uv init` |
| Existing codebase | Manual setup with `pyproject.toml` |
| Simple library | Flat layout in project root |
| Complex project | `src/` layout (modern standard) |
| Monorepo / Workspace | Use `[tool.uv.workspace]` |

### Recommended Default: UV Init for New Projects

For new projects, use `uv init <name>` which automatically creates:
- ✅ `pyproject.toml` with proper configuration
- ✅ `src/` layout following modern standards
- ✅ `__init__.py` for package structure
- ✅ `.python-version` for version pinning
- ✅ `README.md` and `.gitignore`

(Note: The `--package` flag is deprecated; `uv init` now creates a package structure by default.)

### The Correct Mental Model: Dependencies & Architecture

When dealing with multiple related packages (e.g., `ecu-controller` depending on `serial-manager`), choose your architecture based on coupling:

**Scenario A: Independent Packages**
If `serial-manager` is a standalone library used by other projects:
1. Create `serial-manager` separately (`uv init serial-manager`).
2. Create `ecu-controller` separately.
3. In `ecu-controller/pyproject.toml`, add dependency: `dependencies = ["serial-manager"]`.
4. Development install:
   ```bash
   uv pip install -e /path/to/serial-manager
   uv pip install -e /path/to/ecu-controller
   ```

**Scenario B: Monorepo (Tightly Coupled)**
If they are always developed together, use a Workspace:
```
my-project/
├── pyproject.toml (Workspace Root)
└── packages/
    ├── serial-manager/
    └── ecu-controller/
```
(See "Working with Monorepos" section below for setup details).

## Project Structure Requirements

### Standard Package Structure (src/ layout)
````
project_root/
├── pyproject.toml          # Package configuration
├── uv.lock                 # Locked dependencies (auto-generated)
├── .python-version         # Python version pin
├── README.md               # Package documentation
├── LICENSE                 # License file
└── src/
    └── package_name/       # Your package code
        ├── __init__.py     # Package definition
        ├── __main__.py     # Module execution entry (optional)
        └── module.py       # Implementation
````

### Adding Dependencies (Modern Workflow)

Instead of manually editing `pyproject.toml`, use `uv add`:

```bash
# Add runtime dependency
uv add requests numpy

# Add dev dependency
uv add --dev pytest black

# Add optional dependency group
uv add --optional docs sphinx
```
This automatically updates both `pyproject.toml` and `uv.lock`.

### Critical Files Explained

#### 1. `pyproject.toml` - The Heart of Your Package

**Minimal Configuration:**
````toml
[project]
name = "package-name"
version = "0.1.0"
description = "Brief description"
authors = [{name = "Your Name", email = "email@example.com"}]
readme = {file = "README.md", content-type = "text/markdown"}
requires-python = ">=3.11"
dependencies = [
    "dependency>=1.0.0",
]

[project.scripts]
my-command = "package_name.module:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/package_name"]
````

**Entry Points Explanation:**

The `[project.scripts]` section creates CLI commands:
````toml
[project.scripts]
my-command = "package_name.module:main"
````

- `my-command`: The executable name users type in terminal
- `package_name.module:main`: Path to the function to execute
  - Looks in `package_name` package
  - Finds `module.py` file
  - Calls the `main()` function

#### 2. `src/package_name/__init__.py` - Package Definition

**Purpose:** Makes the directory a Python package and defines public API.
````python
"""Package description."""

__version__ = "0.1.0"

from package_name.module import main

__all__ = ["main"]
````

#### 3. `src/package_name/__main__.py` - Module Execution

**Purpose:** Allows running package with `python -m package_name`.
````python
"""Entry point for module execution."""

from package_name.module import main

if __name__ == "__main__":
    main()
````

#### 4. Implementation File with `main()` Function

Your actual code must have a `main()` function for the entry point:
````python
# src/package_name/module.py

def main():
    """Main entry point for the application."""
    # Your application logic
    print("Application running!")

if __name__ == "__main__":
    main()
````

### Improving Package Discoverability

Add these to `pyproject.toml` for better PyPI presentation:
````toml
[project]
keywords = ["keyword1", "keyword2", "topic"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Topic :: Software Development",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
]

[project.urls]
Homepage = "https://github.com/username/project"
Repository = "https://github.com/username/project"
Issues = "https://github.com/username/project/issues"
Documentation = "https://project.readthedocs.io"
````

## Local Testing Steps

### Step 1: Test the Command Locally

Before building, verify everything works:
````bash
# Test the command (uses entry point from pyproject.toml)
uv run my-command

# Test module execution
uv run python -m package_name

# Test imports work
uv run python -c "from package_name import main; print('Import works!')"
````

### Step 2: Configuration for MCP Clients (Before Publishing)

For local development with MCP clients like Claude Desktop:
````json
{
  "mcpServers": {
    "server-name": {
      "command": "uv",
      "args": ["run", "my-command"],
      "cwd": "/absolute/path/to/project/root"
    }
  }
}
````

**Important:** The `cwd` must point to the directory containing `pyproject.toml`.

## Building the Package

### Step 1: Build Distribution Files
````bash
uv build
````

**Output:** Creates `dist/` folder with:
- `package_name-0.1.0-py3-none-any.whl` (Built package/wheel)
- `package_name-0.1.0.tar.gz` (Source distribution)

**Note:** UV automatically installs build dependencies (like hatchling) if needed.

### Step 2: Verify Build Contents
````bash
# List wheel contents
unzip -l dist/package_name-0.1.0-py3-none-any.whl

# Should contain:
# - package_name/
# - package_name-0.1.0.dist-info/
````

## Publishing Workflow

### Step 1: Create PyPI Accounts & Tokens

1. **TestPyPI account:** https://test.pypi.org/account/register/
2. **Real PyPI account:** https://pypi.org/account/register/
3. Enable 2FA on both accounts (required)
4. Generate API tokens for both

### Step 2: Authentication Options

**Option 1: Inline token (one-time)**
```bash
uv publish --token "pypi-..."
```

**Option 2: Environment variable (recommended for CI/CD)**
```bash
export UV_PUBLISH_TOKEN="pypi-..."
uv publish
```

**Option 3: Keyring (for local development)**
UV can use system keyring to store tokens securely.

### Step 3: Publish to TestPyPI First

**Always test on TestPyPI before publishing to real PyPI.**

```bash
# Full URL
uv publish --publish-url https://test.pypi.org/legacy/ --token "pypi-..."

# Or use --test flag (if available in your uv version)
uv publish --test --token "pypi-..."
```

### Step 4: Test Installation from TestPyPI

**Important Limitation:** TestPyPI doesn't have access to packages on real PyPI. If your package has dependencies that only exist on PyPI, you need both indexes:
````bash
# Install with both indexes
pip install --index-url https://test.pypi.org/simple/ \
            --extra-index-url https://pypi.org/simple/ \
            package-name

# Test the command
my-command

# Test with uvx (run without installing)
uvx --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ \
    package-name
````

### Step 5: Publish to Real PyPI

Once TestPyPI verification is complete:
````bash
uv publish --token "pypi-your-real-pypi-token"
````

### Step 6: Verify on PyPI

1. Visit `https://pypi.org/project/package-name/`
2. Check metadata displays correctly
3. Verify README renders properly
4. Test installation:
````bash
# Install from PyPI
pip install package-name

# Or run directly with uvx
uvx package-name
````

### Step 7: Update MCP Client Configuration

After publishing to PyPI, users can use the simple configuration:
````json
{
  "mcpServers": {
    "server-name": {
      "command": "uvx",
      "args": ["package-name"]
    }
  }
}
````

**Comparison of Methods:**

| Method | When to Use | Configuration |
|--------|-------------|---------------|
| `uvx` | After publishing to PyPI | `"command": "uvx", "args": ["package-name"]` |
| `uv run` | Local development | `"command": "uv", "args": ["run", "my-command"], "cwd": "/path"` |
| `python -m` | Manual control | `"command": "python", "args": ["-m", "package_name"]` |
| Direct command | After pip install | `"command": "my-command"` |

## Reproducible Development Setup

Ensure everyone on the team has the exact same environment:

```bash
# Install exact versions from uv.lock
uv sync

# Install with dev dependencies
uv sync --extra dev

# Update dependencies
uv sync --upgrade
```

## Working with Monorepos (Workspaces)

For projects with multiple packages (e.g. `serial-manager` + `ecu-controller`):

```toml
# Root pyproject.toml
[tool.uv.workspace]
members = ["packages/*"]

# Directory structure:
# project/
# ├── pyproject.toml
# └── packages/
#     ├── serial-manager/
#     │   └── pyproject.toml
#     └── ecu-controller/
#         └── pyproject.toml
```

**Build all packages:** `uv build --all`

## Future Updates and Version Management

### Releasing a New Version
````bash
# 1. Update version in pyproject.toml
# [project]
# version = "0.2.0"

# 2. Clean old build
rm -rf dist/ 

# 3. Build the new version
uv build

# 4. Publish to PyPI
uv publish --token "your-pypi-token"

# 5. Create and push Git tag
git tag v0.2.0
git push origin v0.2.0
````

### Semantic Versioning

Follow semantic versioning (semver):
- **0.1.0 → 0.1.1**: Bug fixes (patch)
- **0.1.0 → 0.2.0**: New features (minor)
- **0.9.0 → 1.0.0**: Breaking changes (major)

## Common Pitfalls and Solutions

### 1. UV Cache Issues

**Symptom:** Old versions being used despite updates or weird build artifacts.

**Solution:**
```bash
# Clear UV cache
uv cache clean

# Rebuild with fresh cache
uv build
```

### 2. Import Errors After Installation

**Symptom:** `ModuleNotFoundError` when importing

**Common Causes:**
- Relative imports instead of absolute imports
- Missing `__init__.py`
- Incorrect `packages` in `pyproject.toml`

**Solution:**
````python
# ❌ Wrong - relative import
from .module import function

# ✅ Correct - absolute import
from package_name.module import function
````

### 3. Entry Point Not Working

**Symptom:** Command not found after installation

**Common Causes:**
- Missing `main()` function in target module
- Typo in entry point path
- Entry point pointing to wrong module

**Solution:** Verify entry point matches actual function:
````toml
[project.scripts]
my-command = "package_name.server:main"  # Must have main() in server.py
````

### 4. Package Name vs. Command Name Confusion

**Symptom:** `uvx package_name` fails but `uvx package-name` works

**Explanation:**
````toml
[project]
name = "my_package"  # Package name (PyPI normalizes to my-package)

[project.scripts]
my-command = "my_package.module:main"  # Command users run
````

- Install with: `pip install my-package` (PyPI normalized name)
- Run with: `my-command` (from [project.scripts])
- **Not with:** `my_package` (that's the Python module name)

### 5. Authentication Failures

**Symptom:** `403 Forbidden` or `Invalid authentication`

**Solution:**
````bash
# Username is always __token__ (literally)
# Password is your API token starting with pypi-
uv publish --token "pypi-AgEIcHlwaS5vcmcCJG..."
````

## Verification Strategy

### Pre-Build Checklist

- [ ] `pyproject.toml` has correct name, version, and entry points
- [ ] All `__init__.py` files exist
- [ ] `main()` function exists in entry point target
- [ ] Local testing works: `uv run my-command`
- [ ] Imports work: `uv run python -c "import package_name"`
- [ ] README.md is complete and properly formatted
- [ ] `uv sync` run for reproducible environment

### Pre-Publish Checklist

- [ ] Built successfully: `uv build` completed
- [ ] `dist/` contains .whl and .tar.gz files
- [ ] TestPyPI account created with 2FA enabled
- [ ] API token generated and copied
- [ ] Published to TestPyPI successfully
- [ ] Tested installation from TestPyPI
- [ ] Command works after TestPyPI installation

### Post-Publish Verification

- [ ] Package visible on PyPI: `https://pypi.org/project/package-name/`
- [ ] README renders correctly on PyPI page
- [ ] Metadata is accurate (description, author, links)
- [ ] Installation works: `pip install package-name`
- [ ] Command works: `my-command`
- [ ] `uvx package-name` works without pre-installation

## Installation Methods for Users

### Method 1: uvx (Recommended for End Users)

**Advantages:**
- No installation required
- Always runs latest version
- Isolated environment
- No conflicts with other packages
````bash
uvx package-name
````

**MCP Configuration:**
````json
{
  "mcpServers": {
    "server": {
      "command": "uvx",
      "args": ["package-name"]
    }
  }
}
````

### Method 2: pipx (Alternative)

**Advantages:**
- Isolated environment
- Fast startup after first run
- Widely used
````bash
# Install once
pipx install package-name

# Run anytime
my-command

# Update when needed
pipx upgrade package-name
````

### Method 3: pip with Virtual Environment

**Advantages:**
- Traditional approach
- Full control
- Works everywhere
````bash
# Create and activate venv
python -m venv env
source env/bin/activate  # Linux/Mac
env\Scripts\activate     # Windows

# Install
pip install package-name

# Use
my-command
````

## Documentation Best Practices

### README Structure

Include these sections:

1. **Quick Start** - Immediate installation and usage
2. **Installation** - Multiple methods (uvx, pipx, pip)
3. **Configuration** - For MCP clients or other tools
4. **Usage Examples** - Common use cases
5. **Development** - Contributing guide
6. **License** - License information

### Example README Snippet
````markdown
## Installation

### Quick Start (No Installation Required)
```bash
uvx package-name
```

### Install with pip
```bash
pip install package-name
package-name
```

### For Development
```bash
git clone https://github.com/user/project.git
cd project
pip install -e .
```

## Configuration

For Claude Desktop, add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "server": {
      "command": "uvx",
      "args": ["package-name"]
    }
  }
}
```
````

## Summary Checklist

**Initial Setup:**
- [ ] `pyproject.toml` has correct name, version, and entry points
- [ ] All `__init__.py` files exist
- [ ] `main()` function exists in entry point target
- [ ] Local testing works: `uv run my-command`
- [ ] Imports work: `uv run python -c "import package_name"`
- [ ] README.md is complete and properly formatted
- [ ] `uv sync` run for reproducible environment

**Testing:**
- [ ] Local testing with uv run
- [ ] Imports work correctly
- [ ] Command executes successfully

**Publishing:**
- [ ] Built with uv build
- [ ] Published to TestPyPI
- [ ] Tested from TestPyPI
- [ ] Published to PyPI
- [ ] Verified on PyPI

**Documentation:**
- [ ] README with installation methods
- [ ] Configuration examples
- [ ] GitHub repository topics
- [ ] License file included

**Distribution:**
- [ ] GitHub release created
- [ ] Version tagged
- [ ] Shared with community
