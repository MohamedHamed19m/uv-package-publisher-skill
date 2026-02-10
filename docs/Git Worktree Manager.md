# Git Worktree Manager (WTM)

An interactive CLI tool to streamline the creation and cleanup of Git worktrees. Context-Aware: compares worktrees against your CURRENT branch. Enhanced with Rich library for beautiful CLI output.

## Features

- **List Worktrees** - Display all linked worktrees with merge status and age
- **Create New Worktree** - Create worktrees with chronological naming (e.g., `fix-Feb10-1430-1`)
- **Merge Worktree** - Merge a worktree's branch into your current branch
- **Remove Worktree** - Remove one or more worktrees with optional branch deletion
- **Open in VS Code** - Quickly open a worktree in Visual Studio Code

## Installation

### Best Practice: PowerShell Function

Add this function to your PowerShell profile (run `notepad $PROFILE` to edit):

```powershell
function wtm {
    uv run "C:\Scripts\wtm.py"
}
```

Then simply run `wtm` from any terminal to launch the tool.

## Usage

```
wtm
```

This launches the interactive menu:

```
+-------------------------------------------------------+
|               Git Worktree Manager                    |
+-------+-----------------------------------------------+
| Option | Description                                  |
+-------+-----------------------------------------------+
| 1      | List Worktrees                               |
| 2      | Create New Worktree                          |
| 3      | Merge Worktree into Current                  |
| 4      | Remove Worktree                              |
| 5      | Open Worktree in VS Code                     |
| 6      | Exit                                         |
+-------+-----------------------------------------------+
```

### Menu Options

| Option | Description |
|--------|-------------|
| 1 | List all worktrees with their status (MERGED/NOT MERGED/DETACHED) and age |
| 2 | Create a new worktree from the current branch with auto-generated naming |
| 3 | Merge a selected worktree's branch into your current branch |
| 4 | Remove worktrees (supports ranges like `1-3`, comma-separated like `1,2,3`, or `all`) |
| 5 | Open a worktree directory in VS Code |
| 6 | Exit the tool |

## Worktree Status

The tool shows three types of worktree status:

- **[green]MERGED[/green]** - Branch has been merged into the current parent branch (safe to remove)
- **[yellow]NOT MERGED[/yellow]** - Branch has not been merged (warning before removal)
- **[red]DETACHED[/red]** - Worktree is in detached HEAD state

## Example Workflow

```bash
# Launch the tool
wtm

# Option 2: Create a new worktree (auto-named: fix-Feb10-1430-1)

# ... do your work in the new worktree ...

# Option 3: Merge the worktree back into your current branch

# Option 4: Remove the worktree and delete the branch
```

## Requirements

- Python 3.8+
- Git
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- `rich` library (installed via dependencies in script)
