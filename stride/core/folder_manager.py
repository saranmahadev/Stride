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
from typing import Optional, List, Dict
from enum import Enum
import shutil
import logging

# Set up logging
logger = logging.getLogger(__name__)


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
    
    def validate_structure(self) -> Dict[str, bool]:
        """
        Validate the Stride folder structure.
        
        Returns:
            Dictionary with validation results for each component
        """
        logger.info("Validating Stride folder structure")
        
        results = {
            "stride_root": self.stride_root.exists() and self.stride_root.is_dir(),
            "sprints_root": self.sprints_root.exists() and self.sprints_root.is_dir(),
            "specs_dir": (self.stride_root / "specs").exists(),
            "introspection_dir": (self.stride_root / "introspection").exists(),
        }
        
        # Check all status folders
        for status in SprintStatus:
            status_path = self.sprints_root / status.value
            results[f"status_{status.value}"] = status_path.exists() and status_path.is_dir()
        
        all_valid = all(results.values())
        logger.info(f"Structure validation: {'PASSED' if all_valid else 'FAILED'}")
        
        return results
    
    def list_sprints_by_status(self, status: SprintStatus) -> List[str]:
        """
        List all sprint IDs in a specific status folder.
        
        Args:
            status: Status to list sprints from
            
        Returns:
            List of sprint IDs
        """
        logger.debug(f"Listing sprints in status: {status.value}")
        
        status_folder = self.sprints_root / status.value
        if not status_folder.exists():
            logger.warning(f"Status folder {status.value} does not exist")
            return []
        
        sprints = []
        for sprint_dir in status_folder.iterdir():
            if sprint_dir.is_dir() and sprint_dir.name.startswith("SPRINT-"):
                sprints.append(sprint_dir.name)
        
        logger.debug(f"Found {len(sprints)} sprints in {status.value}")
        return sorted(sprints)
    
    def delete_sprint(self, sprint_id: str, status: Optional[SprintStatus] = None) -> bool:
        """
        Delete a sprint folder (hard delete).
        
        Args:
            sprint_id: Sprint identifier
            status: Optional status if known, otherwise searches all statuses
            
        Returns:
            True if deleted successfully, False if not found
            
        Raises:
            OSError: If deletion fails
        """
        logger.warning(f"Hard delete requested for sprint {sprint_id}")
        
        if status:
            sprint_path = self.get_sprint_path(sprint_id, status)
            if not sprint_path.exists():
                logger.error(f"Sprint {sprint_id} not found in {status.value}")
                return False
        else:
            result = self.find_sprint(sprint_id)
            if not result:
                logger.error(f"Sprint {sprint_id} not found in any status")
                return False
            sprint_path, _ = result
        
        try:
            shutil.rmtree(sprint_path)
            logger.info(f"Deleted sprint {sprint_id} from {sprint_path}")
            return True
        except OSError as e:
            logger.error(f"Failed to delete sprint {sprint_id}: {e}")
            raise
    
    def archive_sprint(self, sprint_id: str, status: Optional[SprintStatus] = None) -> Path:
        """
        Archive a sprint (soft delete) by moving it to .archive folder.
        
        Args:
            sprint_id: Sprint identifier
            status: Optional status if known, otherwise searches all statuses
            
        Returns:
            Path to the archived sprint
            
        Raises:
            FileNotFoundError: If sprint doesn't exist
            OSError: If archiving fails
        """
        logger.info(f"Archiving sprint {sprint_id}")
        
        # Ensure .archive directory exists
        archive_root = self.sprints_root / ".archive"
        archive_root.mkdir(exist_ok=True)
        
        # Find the sprint
        if status:
            sprint_path = self.get_sprint_path(sprint_id, status)
            if not sprint_path.exists():
                raise FileNotFoundError(f"Sprint {sprint_id} not found in {status.value}")
            sprint_status = status
        else:
            result = self.find_sprint(sprint_id)
            if not result:
                raise FileNotFoundError(f"Sprint {sprint_id} not found in any status")
            sprint_path, sprint_status = result
        
        # Create status subfolder in archive
        archive_status_folder = archive_root / sprint_status.value
        archive_status_folder.mkdir(exist_ok=True)
        
        # Move to archive
        archive_path = archive_status_folder / sprint_id
        
        # Handle case where sprint already exists in archive
        if archive_path.exists():
            logger.warning(f"Sprint {sprint_id} already in archive, adding timestamp")
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_path = archive_status_folder / f"{sprint_id}_{timestamp}"
        
        try:
            shutil.move(str(sprint_path), str(archive_path))
            logger.info(f"Archived sprint {sprint_id} to {archive_path}")
            return archive_path
        except OSError as e:
            logger.error(f"Failed to archive sprint {sprint_id}: {e}")
            raise
    
    def restore_sprint(self, sprint_id: str, from_archive_status: SprintStatus) -> Path:
        """
        Restore a sprint from archive back to its original status.
        
        Args:
            sprint_id: Sprint identifier
            from_archive_status: Original status the sprint was in
            
        Returns:
            Path to the restored sprint
            
        Raises:
            FileNotFoundError: If archived sprint doesn't exist
            OSError: If restoration fails
        """
        logger.info(f"Restoring sprint {sprint_id} from archive")
        
        archive_root = self.sprints_root / ".archive"
        archive_path = archive_root / from_archive_status.value / sprint_id
        
        if not archive_path.exists():
            raise FileNotFoundError(f"Archived sprint {sprint_id} not found in .archive/{from_archive_status.value}")
        
        # Destination path
        dest_path = self.get_sprint_path(sprint_id, from_archive_status)
        
        # Check if sprint already exists in target location
        if dest_path.exists():
            raise FileExistsError(f"Sprint {sprint_id} already exists in {from_archive_status.value}")
        
        try:
            shutil.move(str(archive_path), str(dest_path))
            logger.info(f"Restored sprint {sprint_id} to {dest_path}")
            return dest_path
        except OSError as e:
            logger.error(f"Failed to restore sprint {sprint_id}: {e}")
            raise
    
    def get_sprint_count(self, status: Optional[SprintStatus] = None) -> int:
        """
        Get the count of sprints in a specific status or all statuses.
        
        Args:
            status: Optional status to count, None for all statuses
            
        Returns:
            Number of sprints
        """
        if status:
            return len(self.list_sprints_by_status(status))
        
        total = 0
        for s in SprintStatus:
            total += len(self.list_sprints_by_status(s))
        return total
    
    def get_all_sprints_with_status(self) -> Dict[SprintStatus, List[str]]:
        """
        Get all sprints organized by status.
        
        Returns:
            Dictionary mapping status to list of sprint IDs
        """
        logger.debug("Getting all sprints with status")
        
        result = {}
        for status in SprintStatus:
            result[status] = self.list_sprints_by_status(status)
        
        return result
