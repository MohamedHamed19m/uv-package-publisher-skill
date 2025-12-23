---
name: python-package-publishing
description: Streamlined workflow for packaging and distributing Python projects using UV. Use this skill when initializing new libraries, configuring CLI entry points in pyproject.toml, or building and uploading artifacts to PyPI/TestPyPI. Ideal for converting local scripts into installable tools or setting up MCP servers for distribution.

keywords: ["uv build", "pypi publishing", "pyproject.toml", "python packaging", "testpypi"]
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
python --version  # Ensure >= 3.10 for modern packaging
````

**Identify Project Type:**
- Existing codebase vs. new project
- MCP server, CLI tool, library, or application
- Dependencies and their availability on PyPI

## Approach Selection

### Decision Framework

| Condition | Recommended Approach |
|-----------|---------------------|
| New project from scratch | Use `uv init --package` |
| Existing codebase | Manual setup with `pyproject.toml` |
| Simple library | Flat layout in project root |
| Complex project | `src/` layout (modern standard) |
| MCP server | Include entry points for CLI commands |

### Recommended Default: UV Init for New Projects

For new projects, use `uv init --package <name>` which automatically creates:
- ✅ `pyproject.toml` with proper configuration
- ✅ `src/` layout following modern standards
- ✅ `__init__.py` for package structure
- ✅ `.python-version` for version pinning
- ✅ `README.md` and `.gitignore`

## Project Structure Requirements

### Standard Package Structure (src/ layout)
````
project_root/
├── pyproject.toml          # Package configuration
├── README.md               # Package documentation
├── LICENSE                 # License file
└── src/
    └── package_name/       # Your package code
        ├── __init__.py     # Package definition
        ├── __main__.py     # Module execution entry (optional)
        └── module.py       # Implementation
````

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
requires-python = ">=3.10"
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

**Important Naming Convention:**
- **Package name** (in `[project]`): Can use underscores (`my_package`)
- **Command name** (in `[project.scripts]`): Often uses hyphens (`my-command`)
- PyPI normalizes names, so `my_package` becomes `my-package` on PyPI
- The command you run is whatever you specify in `[project.scripts]`

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

**Do You Need This?**
- ⚠️ Optional but recommended
- ✅ Enables `python -m package_name` syntax
- ✅ Useful during development
- ✅ Standard Python convention
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
    "Programming Language :: Python :: 3.10",
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

### Step 2: Verify Build Contents
````bash
# List wheel contents
unzip -l dist/package_name-0.1.0-py3-none-any.whl

# Should contain:
# - package_name/
# - package_name-0.1.0.dist-info/
````

## Publishing Workflow

### Step 1: Create PyPI Accounts

1. **TestPyPI account:** https://test.pypi.org/account/register/
2. **Real PyPI account:** https://pypi.org/account/register/
3. Enable 2FA on both accounts (required)
4. Generate API tokens for both

**Important:** TestPyPI and PyPI are completely separate:
- Different accounts
- Different tokens
- Different package indexes

### Step 2: Publish to TestPyPI First

**Always test on TestPyPI before publishing to real PyPI.**
````bash
uv publish --publish-url https://test.pypi.org/legacy/ --token "pypi-your-testpypi-token"
````

### Step 3: Test Installation from TestPyPI

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

### Step 4: Publish to Real PyPI

Once TestPyPI verification is complete:
````bash
uv publish --token "pypi-your-real-pypi-token"
````

### Step 5: Verify on PyPI

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

### Step 6: Update MCP Client Configuration

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

## Future Updates and Version Management

### Releasing a New Version
````bash
# 1. Update version in pyproject.toml
# [project]
# version = "0.2.0"

# 2. Build the new version
uv build

# 3. Publish to PyPI
uv publish --token "your-pypi-token"

# 4. Create and push Git tag
git tag v0.2.0
git push origin v0.2.0

# 5. Create GitHub release (optional but recommended)
````

### Semantic Versioning

Follow semantic versioning (semver):
- **0.1.0 → 0.1.1**: Bug fixes (patch)
- **0.1.0 → 0.2.0**: New features (minor)
- **0.9.0 → 1.0.0**: Breaking changes (major)

## Common Pitfalls and Solutions

### 1. Import Errors After Installation

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

### 2. Entry Point Not Working

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

### 3. Package Name vs. Command Name Confusion

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

### 4. TestPyPI Dependency Issues

**Symptom:** Cannot install from TestPyPI due to missing dependencies

**Cause:** Dependencies only exist on real PyPI, not TestPyPI

**Solution:** Use both indexes:
````bash
pip install --index-url https://test.pypi.org/simple/ \
            --extra-index-url https://pypi.org/simple/ \
            package-name
````

**Note:** This is expected - TestPyPI is for testing the publishing process, not full dependency resolution.

### 5. Authentication Failures

**Symptom:** `403 Forbidden` or `Invalid authentication`

**Common Causes:**
- Using username/password instead of token
- Token from wrong service (TestPyPI token for PyPI)
- Token not copied completely

**Solution:**
````bash
# Username is always __token__ (literally)
# Password is your API token starting with pypi-
uv publish --token "pypi-AgEIcHlwaS5vcmcCJG..."
````

### 6. `__main__.py` Not Needed But Causes Confusion

**When It Matters:**
- ✅ Needed for `python -m package_name` to work
- ❌ Not needed if only using entry point commands
- ✅ Best practice to include anyway

**Structure:**
````python
# __main__.py
from package_name.module import main

if __name__ == "__main__":
    main()
````

## Verification Strategy

### Pre-Build Checklist

- [ ] `pyproject.toml` has correct name, version, and entry points
- [ ] All `__init__.py` files exist
- [ ] `main()` function exists in entry point target
- [ ] Local testing works: `uv run my-command`
- [ ] Imports work: `uv run python -c "import package_name"`
- [ ] README.md is complete and properly formatted

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

### Method 4: Development Installation

**For contributors and developers:**
````bash
# Clone repository
git clone https://github.com/user/project.git
cd project

# Install in editable mode
pip install -e .

# Changes to code are immediately reflected
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
- [ ] Project structure with src/ layout
- [ ] pyproject.toml configured
- [ ] Entry points defined
- [ ] __init__.py files in place
- [ ] main() function exists

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