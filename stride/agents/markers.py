"""
Managed Marker System for Safe Content Updates

Provides safe insertion and updating of Stride-managed content blocks
while preserving user customizations outside the markers.

Markers:
- <!-- STRIDE:START --> - Beginning of managed block
- <!-- STRIDE:END --> - End of managed block
"""

import os
from typing import Optional, Tuple
from pathlib import Path


class ManagedMarkerSystem:
    """Handles insertion and updating of managed content blocks."""
    
    START_MARKER = "<!-- STRIDE:START -->"
    END_MARKER = "<!-- STRIDE:END -->"
    
    # TOML comment variants for slash command files
    TOML_START_MARKER = "# STRIDE:START"
    TOML_END_MARKER = "# STRIDE:END"
    
    @classmethod
    def has_markers(cls, content: str, file_type: str = "markdown") -> bool:
        """
        Check if content contains managed markers.
        
        Args:
            content: File content to check
            file_type: Type of file ('markdown' or 'toml')
            
        Returns:
            True if both start and end markers are present
        """
        if file_type == "toml":
            return cls.TOML_START_MARKER in content and cls.TOML_END_MARKER in content
        return cls.START_MARKER in content and cls.END_MARKER in content
    
    @classmethod
    def extract_managed_content(cls, content: str, file_type: str = "markdown") -> Optional[str]:
        """
        Extract content between managed markers.
        
        Args:
            content: File content
            file_type: Type of file ('markdown' or 'toml')
            
        Returns:
            Content between markers, or None if markers not found
        """
        start_marker = cls.TOML_START_MARKER if file_type == "toml" else cls.START_MARKER
        end_marker = cls.TOML_END_MARKER if file_type == "toml" else cls.END_MARKER
        
        if not cls.has_markers(content, file_type):
            return None
        
        start_idx = content.find(start_marker) + len(start_marker)
        end_idx = content.find(end_marker)
        
        return content[start_idx:end_idx].strip()
    
    @classmethod
    def insert_managed_content(
        cls,
        new_content: str,
        file_type: str = "markdown",
        existing_content: Optional[str] = None
    ) -> str:
        """
        Insert or update managed content with markers.
        
        Args:
            new_content: New content to insert
            file_type: Type of file ('markdown' or 'toml')
            existing_content: Existing file content (if any)
            
        Returns:
            Complete file content with managed block
        """
        start_marker = cls.TOML_START_MARKER if file_type == "toml" else cls.START_MARKER
        end_marker = cls.TOML_END_MARKER if file_type == "toml" else cls.END_MARKER
        
        wrapped_content = f"{start_marker}\n\n{new_content}\n\n{end_marker}"
        
        # If no existing content, return wrapped content
        if not existing_content:
            return wrapped_content
        
        # If markers don't exist, append at end
        if not cls.has_markers(existing_content, file_type):
            return f"{existing_content}\n\n{wrapped_content}\n"
        
        # Replace content between existing markers
        start_idx = existing_content.find(start_marker)
        end_idx = existing_content.find(end_marker) + len(end_marker)
        
        before = existing_content[:start_idx]
        after = existing_content[end_idx:]
        
        return f"{before}{wrapped_content}{after}"
    
    @classmethod
    def update_file_with_markers(
        cls,
        file_path: Path,
        new_content: str,
        file_type: str = "markdown"
    ) -> Tuple[bool, str]:
        """
        Update a file with managed content, preserving user customizations.
        
        Args:
            file_path: Path to file
            new_content: New managed content to insert
            file_type: Type of file ('markdown' or 'toml')
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # Read existing content if file exists
            existing_content = None
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    existing_content = f.read()
            
            # Generate new content with managed blocks
            updated_content = cls.insert_managed_content(
                new_content,
                file_type,
                existing_content
            )
            
            # Write back to file
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            action = "Updated" if existing_content else "Created"
            return True, f"{action} {file_path.name}"
            
        except Exception as e:
            return False, f"Error updating {file_path.name}: {str(e)}"
    
    @classmethod
    def validate_markers(cls, file_path: Path, file_type: str = "markdown") -> Tuple[bool, str]:
        """
        Validate that a file has correct managed markers.
        
        Args:
            file_path: Path to file to validate
            file_type: Type of file ('markdown' or 'toml')
            
        Returns:
            Tuple of (valid: bool, message: str)
        """
        if not file_path.exists():
            return False, f"File not found: {file_path.name}"
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not cls.has_markers(content, file_type):
                return False, f"Missing managed markers in {file_path.name}"
            
            # Verify markers are properly paired
            start_marker = cls.TOML_START_MARKER if file_type == "toml" else cls.START_MARKER
            end_marker = cls.TOML_END_MARKER if file_type == "toml" else cls.END_MARKER
            
            start_count = content.count(start_marker)
            end_count = content.count(end_marker)
            
            if start_count != 1 or end_count != 1:
                return False, f"Invalid marker count in {file_path.name} (start: {start_count}, end: {end_count})"
            
            # Verify start comes before end
            start_idx = content.find(start_marker)
            end_idx = content.find(end_marker)
            
            if start_idx >= end_idx:
                return False, f"Markers out of order in {file_path.name}"
            
            return True, f"Valid markers in {file_path.name}"
            
        except Exception as e:
            return False, f"Error validating {file_path.name}: {str(e)}"
