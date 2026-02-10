---
summary: "How to create discoverable documentation with YAML front matter metadata for AI context."
read_when: ["creating docs", "documentation", "front matter", "AI context", "readme"]
---

# Creating Discoverable Documentation

Make your markdown files **AI-discoverable** by adding YAML front matter metadata at the top.

## Format

Add this at the **very top** of your markdown file:

```yaml
---
summary: "Brief one-line description of what this doc covers."
read_when: ["trigger1", "trigger2", "trigger3"]
---
```

Then continue with your normal markdown content.

## Fields

| Field | Required | Description |
|-------|----------|-------------|
| `summary` | Yes | One sentence describing the doc's purpose |
| `read_when` | Yes | List of keywords that describe when AI should read this file |

## `read_when` Best Practices

Think: **"When should the AI read this file?"**

Use keywords like:
- **Module names**: `"authentication"`, `"database"`, `"api"`
- **Task types**: `"testing"`, `"debugging"`, `"configuration"`
- **Concepts**: `"setup"`, `"deployment"`, `"security"`

### Examples

| For a file about... | Good `read_when` values |
|---------------------|-------------------------|
| API reference | `["api", "endpoints", "REST", "request"]` |
| Project conventions | `["naming", "conventions", "standards", "style"]` |
| Setup guide | `["setup", "install", "getting started", "configuration"]` |
| Module template | `["template", "new module", "boilerplate"]` |

## Using the Discovery Script

Run the script to see which docs are discoverable:

```bash
# Scan docs/ folder (default)
uv run Scripts/discover.py

# AI-optimized output for system prompts
uv run Scripts/discover.py --ai

# Custom directories
uv run Scripts/discover.py -d docs,src,memory

# Custom project name
uv run Scripts/discover.py -n "MyProject"
```

## Example Complete File

```markdown
---
summary: "Authentication module API reference and usage examples."
read_when: ["auth", "login", "token", "jwt", "authentication"]
---

# Authentication Module

## Overview
This module handles user authentication via JWT tokens.

## Usage
...
```

---

**Note**: Files without front matter `---` blocks are ignored by the discovery script.
