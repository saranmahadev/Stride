"""
SprintManager - Handles sprint lifecycle operations.

Manages sprint creation, metadata, and file operations.
"""
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime, timezone
import logging

from stride.core.folder_manager import FolderManager, SprintStatus
from stride.core.template_engine import TemplateEngine
from stride.core.metadata_manager import MetadataManager

logger = logging.getLogger(__name__)


class SprintManager:
    """Manages sprint lifecycle and metadata operations."""
    
    def __init__(
        self,
        folder_manager: Optional[FolderManager] = None,
        template_engine: Optional[TemplateEngine] = None,
        metadata_manager: Optional[MetadataManager] = None
    ) -> None:
        """
        Initialize the SprintManager.
        
        Args:
            folder_manager: FolderManager instance. Creates new if None.
            template_engine: TemplateEngine instance. Creates new if None.
            metadata_manager: MetadataManager instance. Creates new if None.
        """
        self.folder_manager = folder_manager or FolderManager()
        self.template_engine = template_engine or TemplateEngine()
        self.metadata_manager = metadata_manager or MetadataManager()
        logger.info("SprintManager initialized")
        
    def create_sprint(
        self,
        sprint_id: str,
        title: str,
        description: str,
        author: str,
        status: SprintStatus = SprintStatus.PROPOSED,
        tags: Optional[List[str]] = None,
        priority: str = "medium"
    ) -> Path:
        """
        Create a new sprint with initial metadata using TemplateEngine.
        
        Args:
            sprint_id: Unique sprint identifier
            title: Sprint title
            description: Feature description
            author: User who created the sprint
            status: Initial status (default: PROPOSED)
            tags: Optional list of tags
            priority: Priority level (default: "medium")
            
        Returns:
            Path to the created sprint folder
        """
        logger.info(f"Creating sprint: {sprint_id} with status {status.value}")
        
        # Create sprint folder
        sprint_path = self.folder_manager.create_sprint_folder(sprint_id, status)
        
        # Prepare metadata
        metadata = self.metadata_manager.create_metadata(
            sprint_id=sprint_id,
            title=title,
            status=status.value,
            author=author,
            tags=tags or [],
            priority=priority,
            description=description
        )

        # Render proposal body using template engine
        try:
            proposal_body = self.template_engine.render_proposal(
                sprint_id=sprint_id,
                title=title,
                description=description,
                author=author,
                status=status.value,
                priority=priority
            )
        except TypeError:
            # Older TemplateEngine implementations may expect positional args
            proposal_body = self.template_engine.render_proposal(
                sprint_id, title, description, author
            )

        # Write proposal file with frontmatter using MetadataManager
        proposal_file = sprint_path / "proposal.md"
        self.metadata_manager.write_file(proposal_file, metadata, proposal_body)
        
        logger.info(f"Sprint {sprint_id} created at {sprint_path}")
        return sprint_path
    
    def get_sprint_metadata(self, sprint_id: str) -> Optional[Dict[str, Any]]:
        """
        Read sprint metadata from proposal.md frontmatter using MetadataManager.
        
        Args:
            sprint_id: Sprint identifier
            
        Returns:
            Dictionary of metadata, or None if not found
        """
        logger.debug(f"Getting metadata for sprint: {sprint_id}")
        result = self.folder_manager.find_sprint(sprint_id)
        if not result:
            logger.warning(f"Sprint not found: {sprint_id}")
            return None
            
        sprint_path, _ = result
        proposal_file = sprint_path / "proposal.md"
        
        if not proposal_file.exists():
            logger.warning(f"Proposal file not found: {proposal_file}")
            return None
        
        try:
            metadata, _ = self.metadata_manager.parse_file(proposal_file)
            return metadata
        except Exception as e:
            logger.error(f"Failed to parse metadata for {sprint_id}: {e}")
            return None
    
    def update_sprint_metadata(
        self, 
        sprint_id: str, 
        updates: Dict[str, Any],
        merge: bool = True
    ) -> bool:
        """
        Update sprint metadata in proposal.md using MetadataManager.
        
        Args:
            sprint_id: Sprint identifier
            updates: Dictionary of metadata fields to update
            merge: If True, merge updates. If False, replace metadata.
            
        Returns:
            True if successful, False if sprint not found
        """
        logger.info(f"Updating metadata for sprint: {sprint_id}")
        result = self.folder_manager.find_sprint(sprint_id)
        if not result:
            logger.warning(f"Sprint not found: {sprint_id}")
            return False
            
        sprint_path, _ = result
        proposal_file = sprint_path / "proposal.md"
        
        if not proposal_file.exists():
            logger.warning(f"Proposal file not found: {proposal_file}")
            return False
        
        try:
            # Ensure updated timestamp (timezone-aware UTC)
            if "updated" not in updates:
                updates["updated"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            
            # Update using MetadataManager
            self.metadata_manager.update_frontmatter(
                proposal_file,
                updates,
                merge=merge
            )
            logger.info(f"Metadata updated for sprint: {sprint_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to update metadata for {sprint_id}: {e}")
            return False
    
    def move_sprint_status(
        self,
        sprint_id: str,
        to_status: SprintStatus,
        reason: Optional[str] = None
    ) -> bool:
        """
        Move a sprint to a new status (folder and metadata).
        
        Args:
            sprint_id: Sprint identifier
            to_status: Target status
            reason: Optional reason for transition (e.g., blocking reason)
            
        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Moving sprint {sprint_id} to status: {to_status.value}")
        result = self.folder_manager.find_sprint(sprint_id)
        if not result:
            logger.warning(f"Sprint not found: {sprint_id}")
            return False
            
        _, from_status = result
        
        # Move the sprint folder
        try:
            self.folder_manager.move_sprint(sprint_id, from_status, to_status)
        except Exception as e:
            logger.error(f"Failed to move sprint folder: {e}")
            return False
        
        # Update metadata
        updates = {"status": to_status.value}
        if reason:
            updates["reason"] = reason
            
        success = self.update_sprint_metadata(sprint_id, updates)
        if success:
            logger.info(f"Sprint {sprint_id} moved from {from_status.value} to {to_status.value}")
        return success
    
    def transition_sprint(
        self,
        sprint_id: str,
        to_status: SprintStatus,
        reason: Optional[str] = None
    ) -> bool:
        """
        Alias for move_sprint_status (backward compatibility).
        
        Args:
            sprint_id: Sprint identifier
            to_status: Target status
            reason: Optional reason for transition (e.g., blocking reason)
            
        Returns:
            True if successful, False otherwise
        """
        return self.move_sprint_status(sprint_id, to_status, reason)
    
    def get_sprint(self, sprint_id: str) -> Optional[Dict[str, Any]]:
        """
        Get complete sprint information (path, status, metadata).
        
        Args:
            sprint_id: Sprint identifier
            
        Returns:
            Dictionary with sprint info, or None if not found
        """
        logger.debug(f"Getting sprint: {sprint_id}")
        result = self.folder_manager.find_sprint(sprint_id)
        if not result:
            return None
        
        sprint_path, status = result
        metadata = self.get_sprint_metadata(sprint_id)
        
        return {
            "id": sprint_id,
            "path": sprint_path,
            "status": status,
            "metadata": metadata
        }
    
    def list_all_sprints(self) -> List[Dict[str, Any]]:
        """
        List all sprints across all statuses with their metadata.
        
        Returns:
            List of sprint dictionaries
        """
        logger.debug("Listing all sprints")
        sprints = []
        
        for status in SprintStatus:
            sprint_ids = self.folder_manager.list_sprints_by_status(status)

            for sprint_id in sprint_ids:
                sprint_path = self.folder_manager.get_sprint_path(sprint_id, status)
                metadata = self.get_sprint_metadata(sprint_id)

                sprints.append({
                    "id": sprint_id,
                    "path": sprint_path,
                    "status": status,
                    "metadata": metadata
                })
        
        logger.info(f"Found {len(sprints)} sprints")
        return sprints
    
    def validate_sprint(self, sprint_id: str, strict: bool = False) -> Tuple[bool, List[str]]:
        """
        Validate sprint structure and metadata.
        
        Args:
            sprint_id: Sprint identifier
            strict: If True, require all optional fields
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        logger.debug(f"Validating sprint: {sprint_id}")
        errors = []
        
        # Check if sprint exists
        result = self.folder_manager.find_sprint(sprint_id)
        if not result:
            errors.append(f"Sprint not found: {sprint_id}")
            return False, errors
        
        sprint_path, status = result
        
        # Check proposal.md exists
        proposal_file = sprint_path / "proposal.md"
        if not proposal_file.exists():
            errors.append(f"Missing proposal.md for sprint: {sprint_id}")
            return False, errors
        
        # Validate metadata
        try:
            metadata, _ = self.metadata_manager.parse_file(proposal_file)
            
            # Validate using MetadataManager (raises exception on failure)
            try:
                self.metadata_manager.validate_metadata(metadata, strict=strict)
            except Exception as validation_error:
                errors.append(f"Metadata validation failed: {validation_error}")
            
            # Check status consistency
            if metadata.get("status") != status.value:
                errors.append(
                    f"Status mismatch: metadata={metadata.get('status')}, "
                    f"folder={status.value}"
                )
        except Exception as e:
            errors.append(f"Failed to parse metadata: {e}")
            return False, errors
        
        is_valid = len(errors) == 0
        if is_valid:
            logger.info(f"Sprint {sprint_id} is valid")
        else:
            logger.warning(f"Sprint {sprint_id} validation failed: {errors}")
        
        return is_valid, errors
