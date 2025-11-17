"""
FolderManager - Manages status-based folder structure for sprints.

Handles creation and transition of sprints between:
- proposed/
- active/
- blocked/
- review/
- completed/
"""
from pathlib import Path
from typing import Optional, List
from enum import Enum


class SprintStatus(Enum):
    """Sprint lifecycle status states."""
    PROPOSED = "proposed"
    ACTIVE = "active"
    BLOCKED = "blocked"
    REVIEW = "review"
    COMPLETED = "completed"


class FolderManager:
    """Manages the status-based folder structure for Stride sprints."""
    
    def __init__(self, project_root: Optional[Path] = None) -> None:
        """
        Initialize the FolderManager.
        
        Args:
            project_root: Root directory of the project. Defaults to current directory.
        """
        self.project_root = project_root or Path.cwd()
        self.stride_root = self.project_root / "stride"
        self.sprints_root = self.stride_root / "sprints"
        
    def ensure_structure(self) -> None:
        """
        Ensure all required Stride directories exist.
        Creates the base folder structure if it doesn't exist.
        """
        # Main directories
        self.stride_root.mkdir(exist_ok=True)
        self.sprints_root.mkdir(exist_ok=True)
        
        # Status-based folders
        for status in SprintStatus:
            (self.sprints_root / status.value).mkdir(exist_ok=True)
            
        # Other required directories
        (self.stride_root / "specs").mkdir(exist_ok=True)
        (self.stride_root / "introspection").mkdir(exist_ok=True)
    
    def get_sprint_path(self, sprint_id: str, status: SprintStatus) -> Path:
        """
        Get the full path to a sprint folder.
        
        Args:
            sprint_id: Sprint identifier (e.g., "SPRINT-7K9P")
            status: Current status of the sprint
            
        Returns:
            Path to the sprint folder
        """
        return self.sprints_root / status.value / sprint_id
    
    def create_sprint_folder(self, sprint_id: str, status: SprintStatus) -> Path:
        """
        Create a new sprint folder in the specified status.
        
        Args:
            sprint_id: Sprint identifier
            status: Initial status for the sprint
            
        Returns:
            Path to the created sprint folder
        """
        sprint_path = self.get_sprint_path(sprint_id, status)
        sprint_path.mkdir(parents=True, exist_ok=True)
        return sprint_path
    
    def move_sprint(
        self, 
        sprint_id: str, 
        from_status: SprintStatus, 
        to_status: SprintStatus
    ) -> Path:
        """
        Move a sprint from one status folder to another.
        
        Args:
            sprint_id: Sprint identifier
            from_status: Current status
            to_status: Target status
            
        Returns:
            New path to the sprint folder
            
        Raises:
            FileNotFoundError: If the sprint doesn't exist in from_status
        """
        source = self.get_sprint_path(sprint_id, from_status)
        destination = self.get_sprint_path(sprint_id, to_status)
        
        if not source.exists():
            raise FileNotFoundError(f"Sprint {sprint_id} not found in {from_status.value}/")
        
        # Move the entire sprint folder
        source.rename(destination)
        return destination
    
    def find_sprint(self, sprint_id: str) -> Optional[tuple[Path, SprintStatus]]:
        """
        Find a sprint across all status folders.
        
        Args:
            sprint_id: Sprint identifier to search for
            
        Returns:
            Tuple of (path, status) if found, None otherwise
        """
        for status in SprintStatus:
            sprint_path = self.get_sprint_path(sprint_id, status)
            if sprint_path.exists():
                return (sprint_path, status)
        return None
    
    def list_sprints(self, status: Optional[SprintStatus] = None) -> List[tuple[str, SprintStatus]]:
        """
        List all sprints, optionally filtered by status.
        
        Args:
            status: Optional status filter
            
        Returns:
            List of tuples containing (sprint_id, status)
        """
        sprints = []
        statuses = [status] if status else list(SprintStatus)
        
        for s in statuses:
            status_folder = self.sprints_root / s.value
            if status_folder.exists():
                for sprint_dir in status_folder.iterdir():
                    if sprint_dir.is_dir():
                        sprints.append((sprint_dir.name, s))
        
        return sprints
    
    def sprint_exists(self, sprint_id: str, status: Optional[SprintStatus] = None) -> bool:
        """
        Check if a sprint exists.
        
        Args:
            sprint_id: Sprint identifier
            status: Optional status to check in specific folder
            
        Returns:
            True if sprint exists, False otherwise
        """
        if status:
            return self.get_sprint_path(sprint_id, status).exists()
        return self.find_sprint(sprint_id) is not None
