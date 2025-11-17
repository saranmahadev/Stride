"""
File Utilities - Helper functions for file operations.
"""
from pathlib import Path
from typing import Optional, Dict, Any
import yaml


def ensure_directory(path: Path) -> None:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        path: Directory path to ensure
    """
    path.mkdir(parents=True, exist_ok=True)


def read_yaml_frontmatter(file_path: Path) -> Optional[Dict[str, Any]]:
    """
    Read YAML frontmatter from a markdown file.
    
    Args:
        file_path: Path to the markdown file
        
    Returns:
        Dictionary of metadata, or None if no frontmatter found
    """
    if not file_path.exists():
        return None
    
    content = file_path.read_text(encoding="utf-8")
    
    if not content.startswith("---"):
        return None
    
    # Split by --- to extract frontmatter
    parts = content.split("---", 2)
    if len(parts) < 2:
        return None
    
    try:
        metadata = yaml.safe_load(parts[1])
        return metadata if isinstance(metadata, dict) else None
    except yaml.YAMLError:
        return None


def write_yaml_frontmatter(
    file_path: Path,
    metadata: Dict[str, Any],
    content: str = ""
) -> None:
    """
    Write markdown file with YAML frontmatter.
    
    Args:
        file_path: Path to write the file
        metadata: Dictionary of metadata for frontmatter
        content: Body content to write after frontmatter
    """
    yaml_str = yaml.dump(metadata, default_flow_style=False, sort_keys=False)
    full_content = f"---\n{yaml_str}---\n{content}"
    file_path.write_text(full_content, encoding="utf-8")


def safe_read_file(file_path: Path, default: str = "") -> str:
    """
    Safely read a file, returning default if file doesn't exist.
    
    Args:
        file_path: Path to the file
        default: Default value if file doesn't exist
        
    Returns:
        File content or default value
    """
    try:
        return file_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return default
    except Exception:
        return default


def file_exists_and_not_empty(file_path: Path) -> bool:
    """
    Check if file exists and is not empty.
    
    Args:
        file_path: Path to check
        
    Returns:
        True if file exists and has content, False otherwise
    """
    return file_path.exists() and file_path.stat().st_size > 0


def get_file_size_human(file_path: Path) -> str:
    """
    Get human-readable file size.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Human-readable size string (e.g., "1.5 KB", "2.3 MB")
    """
    if not file_path.exists():
        return "0 B"
    
    size = file_path.stat().st_size
    
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    
    return f"{size:.1f} TB"
