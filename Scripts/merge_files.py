from pathlib import Path
from typing import Optional

def combine_files_by_extension(extension: str, output_filename: Optional[str] = None) -> None:
    """
    Combines all files of a specific extension in the current directory into one.
    
    Args:
        extension: The file extension to look for (e.g., 'py', 'md', 'txt').
        output_filename: Optional custom name for the output file.
    """
    # Clean up the extension input
    ext = extension.strip().lower()
    if not ext.startswith("."):
        ext = f".{ext}"
    
    # Default output name if none provided (e.g., combined_md_files.txt)
    if not output_filename:
        output_filename = f"combined_{ext[1:]}_files.txt"

    output_path = Path(output_filename).resolve()
    current_dir = Path.cwd()
    
    # Locate files (excluding the output file itself)
    target_files = [f for f in current_dir.rglob(f"*{ext}") if f.resolve() != output_path]

    if not target_files:
        print(f"No {ext} files found in {current_dir}")
        return

    try:
        with output_path.open("w", encoding="utf-8") as outfile:
            for file_path in sorted(target_files):  # Sorted for consistent output
                abs_path = file_path.resolve()
                
                # Professional Header
                outfile.write(f"{'='*80}\n")
                outfile.write(f"FILE: {file_path.name}\n")
                outfile.write(f"PATH: {abs_path}\n")
                outfile.write(f"{'='*80}\n\n")
                
                try:
                    content = file_path.read_text(encoding="utf-8")
                    outfile.write(content)
                except Exception as e:
                    outfile.write(f"!!! Error reading file: {e}\n")
                
                outfile.write("\n\n")
                
        print(f"Successfully combined {len(target_files)} '{ext}' files into: {output_filename}")

    except Exception as e:
        print(f"Critical error: {e}")

if __name__ == "__main__":
    # Get user input for flexibility
    user_ext = input("Enter file extension to combine (e.g., py, md, txt): ")
    combine_files_by_extension(user_ext)