# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "typer>=0.9.0",
#     "pyyaml>=6.0",
# ]
# ///

"""
Context Discovery Script - Generic tool for any repository.
Scans markdown files for YAML front matter and generates AI-optimized context lists.

Usage:
    uv run discover.py                    # Human-readable list
    uv run discover.py --ai               # AI-optimized format
    uv run discover.py --dirs docs,src    # Custom directories
"""

from pathlib import Path
from typing import Optional, Dict, Any, List
import typer
import yaml

app = typer.Typer(
    name="discover",
    help="Discover project documentation with front matter metadata",
    add_completion=False,
)


def extract_front_matter(md_file: Path) -> Optional[Dict[str, Any]]:
    """Efficiently extract YAML front matter without reading the whole file."""
    lines = []
    try:
        with md_file.open("r", encoding="utf-8") as f:
            first_line = f.readline().strip()
            if first_line != "---":
                return None

            for line in f:
                stripped = line.strip()
                if stripped == "---":
                    break
                lines.append(line)
            else:
                return None

        return yaml.safe_load("".join(lines))
    except Exception:
        return None


def discover_docs(root_dir: Path, search_dirs: List[str]) -> List[Dict[str, Any]]:
    """Scan directories for markdown files with front matter."""
    docs = []
    dirs_to_search = [root_dir / d for d in search_dirs]

    for search_dir in dirs_to_search:
        if not search_dir.exists():
            continue

        for md_file in search_dir.rglob("*.md"):
            # Skip noise files
            if any(
                x in md_file.name.lower()
                for x in ["changelog", "license", "contributing"]
            ):
                continue

            front_matter = extract_front_matter(md_file)
            if not front_matter:
                continue

            # Normalize triggers to a list
            read_when = front_matter.get("read_when", [])
            if isinstance(read_when, str):
                read_when = [read_when]

            docs.append(
                {
                    "path": md_file.relative_to(root_dir).as_posix(),
                    "summary": front_matter.get("summary", "No summary"),
                    "read_when": read_when,
                }
            )

    return docs


def print_list(docs: List[Dict[str, Any]], project_name: str) -> None:
    """Print simple list format."""
    if not docs:
        typer.secho("No documentation with front matter found.", fg=typer.colors.YELLOW)
        return

    typer.secho("\n" + "=" * 70, fg=typer.colors.CYAN)
    typer.secho(f"  {project_name.upper()} - DOCUMENTATION INDEX", bold=True, fg=typer.colors.CYAN)
    typer.secho("=" * 70 + "\n", fg=typer.colors.CYAN)

    for doc in sorted(docs, key=lambda x: x["path"]):
        typer.secho(doc["path"], fg=typer.colors.GREEN, bold=True)
        typer.echo(f"  Summary: {doc['summary']}")
        read_when = ", ".join(doc["read_when"]) if doc["read_when"] else "N/A"
        typer.echo(f"  Trigger: {read_when}\n")


def print_ai_format(docs: List[Dict[str, Any]]) -> None:
    """Print format for AI system prompts."""
    if not docs:
        return

    typer.echo("\n# PROJECT CONTEXT GUIDE")
    typer.echo(
        "Review this list. Read the full content of a file ONLY if the current task matches its 'Read when' trigger.\n"
    )

    for doc in sorted(docs, key=lambda x: x["path"]):
        typer.echo(f"FILE: {doc['path']}")
        typer.echo(f"DESC: {doc['summary']}")
        read_when = ", ".join(doc["read_when"]) if doc["read_when"] else "N/A"
        typer.echo(f"WHEN: {read_when}\n")


@app.command()
def main(
    ai: bool = typer.Option(False, "--ai", help="Output in AI-optimized format"),
    root: str = typer.Option(".", "--root", "-r", help="Root project directory"),
    dirs: str = typer.Option(
        "docs",
        "--dirs",
        "-d",
        help="Comma-separated directories to scan (default: docs)",
    ),
    name: str = typer.Option(
        "Project",
        "--name",
        "-n",
        help="Project name for display header",
    ),
) -> None:
    """
    Discover project docs and generate context lists for AI or humans.

    Examples:
        discover.py                         # Scan docs/ folder
        discover.py --ai                    # AI-optimized output
        discover.py -d docs,src,memory      # Multiple directories
        discover.py -n "MyApp"              # Custom project name
    """
    root_dir = Path(root).resolve()
    search_dirs = [d.strip() for d in dirs.split(",")]
    docs = discover_docs(root_dir, search_dirs)

    if ai:
        print_ai_format(docs)
    else:
        print_list(docs, name)


if __name__ == "__main__":
    app()
