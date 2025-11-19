"""
MetadataManager - Handles YAML frontmatter parsing and validation.

Manages sprint metadata in YAML frontmatter format:
---
id: SPRINT-XXXX
title: Sprint title
status: active
created: 2025-11-17T10:00:00Z
---
"""
from pathlib import Path
from typing import Dict, Any, Optional
import yaml
from datetime import datetime, timezone
import logging
import re

logger = logging.getLogger(__name__)


class MetadataValidationError(Exception):
    """Raised when metadata validation fails."""
    pass


class MetadataManager:
    """Manages YAML frontmatter in markdown files."""
    
    # Required fields for sprint metadata
    REQUIRED_FIELDS = {"id", "title", "status", "created"}
    
    # Valid status values
    VALID_STATUSES = {"proposed", "active", "blocked", "review", "completed"}
    
    @staticmethod
    def parse_frontmatter(content: str) -> tuple[Dict[str, Any], str]:
        """
        Parse YAML frontmatter from markdown content.
        
        Args:
            content: Markdown content with YAML frontmatter
            
        Returns:
            Tuple of (metadata dict, body content)
            
        Raises:
            ValueError: If frontmatter format is invalid
            yaml.YAMLError: If YAML parsing fails
        """
        logger.debug("Parsing YAML frontmatter")
        
        # Check for frontmatter delimiters
        if not content.startswith("---"):
            logger.warning("No frontmatter found in content")
            return {}, content
        
        # Find the closing delimiter
        parts = content.split("---", 2)
        if len(parts) < 3:
            raise ValueError("Invalid frontmatter format: missing closing ---")
        
        frontmatter_str = parts[1].strip()
        body = parts[2].strip()
        
        try:
            metadata = yaml.safe_load(frontmatter_str)
            if metadata is None:
                metadata = {}
            
            logger.debug(f"Parsed frontmatter with {len(metadata)} fields")
            return metadata, body
            
        except yaml.YAMLError as e:
            logger.error(f"Failed to parse YAML frontmatter: {e}")
            raise
    
    @staticmethod
    def serialize_frontmatter(metadata: Dict[str, Any], body: str) -> str:
        """
        Serialize metadata and body back to markdown with YAML frontmatter.
        
        Args:
            metadata: Metadata dictionary
            body: Markdown body content
            
        Returns:
            Complete markdown content with frontmatter
        """
        logger.debug("Serializing frontmatter")
        
        yaml_str = yaml.dump(
            metadata,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True
        )
        
        return f"---\n{yaml_str}---\n\n{body}"
    
    @staticmethod
    def parse_file(file_path: Path) -> tuple[Dict[str, Any], str]:
        """
        Parse YAML frontmatter from a markdown file.
        
        Args:
            file_path: Path to markdown file
            
        Returns:
            Tuple of (metadata dict, body content)
            
        Raises:
            FileNotFoundError: If file doesn't exist
        """
        logger.debug(f"Parsing frontmatter from file: {file_path}")
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        content = file_path.read_text(encoding="utf-8")
        return MetadataManager.parse_frontmatter(content)
    
    @staticmethod
    def write_file(file_path: Path, metadata: Dict[str, Any], body: str) -> None:
        """
        Write metadata and body to a markdown file.
        
        Args:
            file_path: Path to markdown file
            metadata: Metadata dictionary
            body: Markdown body content
        """
        logger.debug(f"Writing frontmatter to file: {file_path}")
        
        content = MetadataManager.serialize_frontmatter(metadata, body)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        
        logger.info(f"Wrote frontmatter to {file_path}")
    
    @staticmethod
    def update_frontmatter(
        file_path: Path,
        updates: Dict[str, Any],
        merge: bool = True
    ) -> Dict[str, Any]:
        """
        Update frontmatter in an existing file.
        
        Args:
            file_path: Path to markdown file
            updates: Dictionary of updates to apply
            merge: If True, merge with existing metadata; if False, replace
            
        Returns:
            Updated metadata dictionary
            
        Raises:
            FileNotFoundError: If file doesn't exist
        """
        logger.info(f"Updating frontmatter in {file_path}")
        
        metadata, body = MetadataManager.parse_file(file_path)
        
        if merge:
            metadata.update(updates)
        else:
            metadata = updates
        
        MetadataManager.write_file(file_path, metadata, body)
        
        logger.debug(f"Updated {len(updates)} frontmatter fields")
        return metadata
    
    @staticmethod
    def validate_metadata(metadata: Dict[str, Any], strict: bool = True) -> bool:
        """
        Validate sprint metadata.
        
        Args:
            metadata: Metadata dictionary to validate
            strict: If True, enforce all validation rules; if False, only check required fields
            
        Returns:
            True if valid
            
        Raises:
            MetadataValidationError: If validation fails
        """
        logger.debug("Validating metadata")
        
        # Check required fields
        missing_fields = MetadataManager.REQUIRED_FIELDS - metadata.keys()
        if missing_fields:
            raise MetadataValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )
        
        # Validate ID format (SPRINT-XXXX)
        sprint_id = metadata.get("id", "")
        if not re.match(r"^SPRINT-[A-Z0-9]{4,}$", sprint_id):
            raise MetadataValidationError(
                f"Invalid sprint ID format: {sprint_id}"
            )
        
        # Validate status
        status = metadata.get("status", "")
        if status not in MetadataManager.VALID_STATUSES:
            raise MetadataValidationError(
                f"Invalid status: {status}. Must be one of {MetadataManager.VALID_STATUSES}"
            )
        
        if strict:
            # Validate title is not empty
            if not metadata.get("title", "").strip():
                raise MetadataValidationError("Title cannot be empty")
            
            # Validate created timestamp format
            created = metadata.get("created", "")
            if isinstance(created, str):
                try:
                    datetime.fromisoformat(created.replace("Z", "+00:00"))
                except ValueError:
                    raise MetadataValidationError(
                        f"Invalid created timestamp format: {created}"
                    )
        
        logger.debug("Metadata validation passed")
        return True
    
    @staticmethod
    def create_metadata(
        sprint_id: str,
        title: str,
        status: str = "proposed",
        author: Optional[str] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """
        Create a new metadata dictionary with defaults.
        
        Args:
            sprint_id: Sprint identifier
            title: Sprint title
            status: Sprint status (default: proposed)
            author: Author email (optional)
            **kwargs: Additional metadata fields
            
        Returns:
            Metadata dictionary
        """
        logger.debug(f"Creating metadata for {sprint_id}")
        
        # Use timezone-aware UTC timestamp
        now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        
        metadata = {
            "id": sprint_id,
            "title": title,
            "status": status,
            "created": now,
            "updated": now,
            **kwargs
        }
        
        if author:
            metadata["author"] = author
        
        return metadata
    
    @staticmethod
    def merge_metadata(
        base: Dict[str, Any],
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Merge two metadata dictionaries.
        
        Args:
            base: Base metadata dictionary
            updates: Updates to merge in
            
        Returns:
            Merged metadata dictionary
        """
        logger.debug("Merging metadata dictionaries")
        
        merged = base.copy()
        merged.update(updates)
        
        # Always update the 'updated' timestamp (timezone-aware UTC)
        merged["updated"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        
        return merged
    
    @staticmethod
    def extract_field(file_path: Path, field: str) -> Optional[Any]:
        """
        Extract a specific field from file frontmatter.
        
        Args:
            file_path: Path to markdown file
            field: Field name to extract
            
        Returns:
            Field value, or None if not found
        """
        logger.debug(f"Extracting field '{field}' from {file_path}")
        
        try:
            metadata, _ = MetadataManager.parse_file(file_path)
            return metadata.get(field)
        except Exception as e:
            logger.error(f"Failed to extract field '{field}': {e}")
            return None
    
    @staticmethod
    def validate_file(file_path: Path, strict: bool = True) -> bool:
        """
        Validate frontmatter in a file.
        
        Args:
            file_path: Path to markdown file
            strict: If True, enforce all validation rules
            
        Returns:
            True if valid
            
        Raises:
            MetadataValidationError: If validation fails
            FileNotFoundError: If file doesn't exist
        """
        logger.debug(f"Validating file: {file_path}")
        
        metadata, _ = MetadataManager.parse_file(file_path)
        return MetadataManager.validate_metadata(metadata, strict=strict)
    
    @staticmethod
    def add_event(
        file_path: Path,
        event_type: str,
        message: str,
        metadata_dict: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Add an event to the sprint's timeline.
        
        Args:
            file_path: Path to sprint's proposal.md file
            event_type: Type of event (created, status_changed, updated, etc.)
            message: Human-readable event description
            metadata_dict: Optional additional metadata for the event
        """
        logger.debug(f"Adding event '{event_type}' to {file_path}")
        
        try:
            metadata, body = MetadataManager.parse_file(file_path)
            
            # Initialize events list if it doesn't exist
            if "events" not in metadata:
                metadata["events"] = []
            
            # Create event record
            event = {
                "type": event_type,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "message": message
            }
            
            # Add optional metadata
            if metadata_dict:
                event["metadata"] = metadata_dict
            
            # Append event
            metadata["events"].append(event)
            
            # Write back
            MetadataManager.write_file(file_path, metadata, body)
            
            logger.info(f"Added event '{event_type}' to sprint timeline")
            
        except Exception as e:
            logger.error(f"Failed to add event: {e}")
            raise
    
    @staticmethod
    def get_events(file_path: Path) -> list:
        """
        Get all events from a sprint's timeline.
        
        Args:
            file_path: Path to sprint's proposal.md file
            
        Returns:
            List of event dictionaries
        """
        logger.debug(f"Getting events from {file_path}")
        
        try:
            metadata, _ = MetadataManager.parse_file(file_path)
            return metadata.get("events", [])
        except Exception as e:
            logger.error(f"Failed to get events: {e}")
            return []
