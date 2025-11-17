"""
SprintManager - Handles sprint lifecycle operations.

Manages sprint creation, metadata, and file operations.
"""
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
import yaml

from stride.core.folder_manager import FolderManager, SprintStatus


class SprintManager:
    """Manages sprint lifecycle and metadata operations."""
    
    def __init__(self, folder_manager: Optional[FolderManager] = None) -> None:
        """
        Initialize the SprintManager.
        
        Args:
            folder_manager: FolderManager instance. Creates new if None.
        """
        self.folder_manager = folder_manager or FolderManager()
        
    def create_sprint(
        self,
        sprint_id: str,
        title: str,
        description: str,
        author: str,
        status: SprintStatus = SprintStatus.PROPOSED
    ) -> Path:
        """
        Create a new sprint with initial metadata.
        
        Args:
            sprint_id: Unique sprint identifier
            title: Sprint title
            description: Feature description
            author: User who created the sprint
            status: Initial status (default: PROPOSED)
            
        Returns:
            Path to the created sprint folder
        """
        # Create sprint folder
        sprint_path = self.folder_manager.create_sprint_folder(sprint_id, status)
        
        # Create proposal.md with frontmatter
        metadata = {
            "id": sprint_id,
            "title": title,
            "status": status.value,
            "created": datetime.utcnow().isoformat() + "Z",
            "author": author,
            "updated": datetime.utcnow().isoformat() + "Z",
        }
        
        proposal_content = self._generate_frontmatter(metadata)
        proposal_content += f"\n\n# {title}\n\n{description}\n"
        
        proposal_file = sprint_path / "proposal.md"
        proposal_file.write_text(proposal_content, encoding="utf-8")
        
        return sprint_path
    
    def get_sprint_metadata(self, sprint_id: str) -> Optional[Dict[str, Any]]:
        """
        Read sprint metadata from proposal.md frontmatter.
        
        Args:
            sprint_id: Sprint identifier
            
        Returns:
            Dictionary of metadata, or None if not found
        """
        result = self.folder_manager.find_sprint(sprint_id)
        if not result:
            return None
            
        sprint_path, _ = result
        proposal_file = sprint_path / "proposal.md"
        
        if not proposal_file.exists():
            return None
            
        return self._read_frontmatter(proposal_file)
    
    def update_sprint_metadata(
        self, 
        sprint_id: str, 
        updates: Dict[str, Any]
    ) -> bool:
        """
        Update sprint metadata in proposal.md.
        
        Args:
            sprint_id: Sprint identifier
            updates: Dictionary of metadata fields to update
            
        Returns:
            True if successful, False if sprint not found
        """
        result = self.folder_manager.find_sprint(sprint_id)
        if not result:
            return False
            
        sprint_path, _ = result
        proposal_file = sprint_path / "proposal.md"
        
        if not proposal_file.exists():
            return False
        
        # Read current content
        content = proposal_file.read_text(encoding="utf-8")
        metadata = self._read_frontmatter(proposal_file)
        
        if metadata is None:
            return False
        
        # Update metadata
        metadata.update(updates)
        metadata["updated"] = datetime.utcnow().isoformat() + "Z"
        
        # Extract body (everything after frontmatter)
        if content.startswith("---"):
            parts = content.split("---", 2)
            body = parts[2] if len(parts) > 2 else ""
        else:
            body = content
        
        # Write updated content
        new_content = self._generate_frontmatter(metadata) + body
        proposal_file.write_text(new_content, encoding="utf-8")
        
        return True
    
    def transition_sprint(
        self,
        sprint_id: str,
        to_status: SprintStatus,
        reason: Optional[str] = None
    ) -> bool:
        """
        Transition a sprint to a new status.
        
        Args:
            sprint_id: Sprint identifier
            to_status: Target status
            reason: Optional reason for transition (e.g., blocking reason)
            
        Returns:
            True if successful, False otherwise
        """
        result = self.folder_manager.find_sprint(sprint_id)
        if not result:
            return False
            
        _, from_status = result
        
        # Move the sprint folder
        self.folder_manager.move_sprint(sprint_id, from_status, to_status)
        
        # Update metadata
        updates = {"status": to_status.value}
        if reason:
            updates["reason"] = reason
            
        return self.update_sprint_metadata(sprint_id, updates)
    
    @staticmethod
    def _generate_frontmatter(metadata: Dict[str, Any]) -> str:
        """
        Generate YAML frontmatter block.
        
        Args:
            metadata: Dictionary of metadata
            
        Returns:
            Formatted frontmatter string
        """
        yaml_str = yaml.dump(metadata, default_flow_style=False, sort_keys=False)
        return f"---\n{yaml_str}---"
    
    @staticmethod
    def _read_frontmatter(file_path: Path) -> Optional[Dict[str, Any]]:
        """
        Read YAML frontmatter from a markdown file.
        
        Args:
            file_path: Path to the markdown file
            
        Returns:
            Dictionary of metadata, or None if no frontmatter found
        """
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
