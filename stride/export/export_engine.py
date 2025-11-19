"""
Export engine for Stride sprint data.

Provides flexible data export with multiple formats (JSON, Markdown, CSV, HTML),
filtering capabilities, and template support for reporting and integration.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

from stride.core.sprint_manager import SprintManager
from stride.core.folder_manager import FolderManager, SprintStatus


class ExportFilter:
    """Filter criteria for sprint export."""
    
    def __init__(
        self,
        status: Optional[List[SprintStatus]] = None,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
        author: Optional[str] = None,
        priority: Optional[str] = None,
        tags: Optional[List[str]] = None,
        agents: Optional[List[str]] = None,
    ):
        """
        Initialize export filter.
        
        Args:
            status: Filter by sprint status(es)
            since: Filter sprints created since this date
            until: Filter sprints created until this date
            author: Filter by author email
            priority: Filter by priority level
            tags: Filter by tags (any match)
            agents: Filter by configured agents (any match)
        """
        self.status = status
        self.since = since
        self.until = until
        self.author = author
        self.priority = priority
        self.tags = tags
        self.agents = agents
    
    def matches(self, sprint_data: Dict[str, Any]) -> bool:
        """
        Check if a sprint matches the filter criteria.
        
        Args:
            sprint_data: Sprint information dictionary
            
        Returns:
            True if sprint matches all filter criteria
        """
        metadata = sprint_data.get("metadata", {})
        
        # Status filter
        if self.status and sprint_data.get("status") not in self.status:
            return False
        
        # Date filters
        if self.since or self.until:
            created_str = metadata.get("created")
            if not created_str:
                return False
            
            try:
                created = datetime.fromisoformat(created_str.replace('Z', '+00:00'))
                # Make timezone-aware datetimes for comparison if needed
                if self.since:
                    since_aware = self.since if self.since.tzinfo else self.since.replace(tzinfo=created.tzinfo)
                    if created < since_aware:
                        return False
                if self.until:
                    until_aware = self.until if self.until.tzinfo else self.until.replace(tzinfo=created.tzinfo)
                    if created > until_aware:
                        return False
            except (ValueError, AttributeError):
                return False
        
        # Author filter
        if self.author:
            sprint_author = metadata.get("author", "").lower()
            if self.author.lower() not in sprint_author:
                return False
        
        # Priority filter
        if self.priority:
            sprint_priority = metadata.get("priority", "").lower()
            if sprint_priority != self.priority.lower():
                return False
        
        # Tags filter (any match)
        if self.tags:
            sprint_tags = [tag.lower() for tag in metadata.get("tags", [])]
            if not any(tag.lower() in sprint_tags for tag in self.tags):
                return False
        
        # Agents filter (any match)
        if self.agents:
            sprint_agents = [agent.lower() for agent in metadata.get("agents", [])]
            if not any(agent.lower() in sprint_agents for agent in self.agents):
                return False
        
        return True


class ExportFormatter(ABC):
    """Base class for export formatters."""
    
    @abstractmethod
    def format(self, sprints: List[Dict[str, Any]], metadata: Dict[str, Any]) -> str:
        """
        Format sprint data for export.
        
        Args:
            sprints: List of sprint data dictionaries
            metadata: Export metadata (timestamp, filters, counts, etc.)
            
        Returns:
            Formatted export data as string
        """
        pass
    
    @abstractmethod
    def get_extension(self) -> str:
        """Get file extension for this format (e.g., 'json', 'md')."""
        pass


class ExportEngine:
    """Engine for exporting sprint data in various formats."""
    
    def __init__(self, sprint_manager: SprintManager, folder_manager: FolderManager):
        """
        Initialize export engine.
        
        Args:
            sprint_manager: Sprint manager instance
            folder_manager: Folder manager instance
        """
        self.sprint_manager = sprint_manager
        self.folder_manager = folder_manager
        self.formatters: Dict[str, ExportFormatter] = {}
    
    def register_formatter(self, name: str, formatter: ExportFormatter) -> None:
        """
        Register an export formatter.
        
        Args:
            name: Format name (e.g., 'json', 'markdown', 'csv', 'html')
            formatter: Formatter instance
        """
        self.formatters[name] = formatter
    
    def export(
        self,
        format_name: str,
        filter_criteria: Optional[ExportFilter] = None,
        output_path: Optional[Path] = None,
    ) -> str:
        """
        Export sprint data in specified format.
        
        Args:
            format_name: Name of registered formatter to use
            filter_criteria: Optional filter to apply to sprints
            output_path: Optional path to write output file
            
        Returns:
            Formatted export data as string
            
        Raises:
            ValueError: If format not registered
        """
        if format_name not in self.formatters:
            available = ", ".join(self.formatters.keys())
            raise ValueError(f"Unknown format: {format_name}. Available: {available}")
        
        formatter = self.formatters[format_name]
        
        # Get all sprints
        all_sprints = self.sprint_manager.list_sprints()
        
        # Apply filters
        if filter_criteria:
            filtered_sprints = [s for s in all_sprints if filter_criteria.matches(s)]
        else:
            filtered_sprints = all_sprints
        
        # Load full sprint data
        full_sprint_data = []
        for sprint in filtered_sprints:
            sprint_id = sprint["id"]
            sprint_info = self.sprint_manager.get_sprint(sprint_id)
            
            if sprint_info:
                # Add file contents
                sprint_path = sprint_info["path"]
                files_content = {}
                
                for file_name in ["proposal.md", "plan.md", "design.md", 
                                 "implementation.md", "retrospective.md"]:
                    file_path = sprint_path / file_name
                    if file_path.exists():
                        try:
                            files_content[file_name] = file_path.read_text(encoding="utf-8")
                        except Exception:
                            files_content[file_name] = None
                
                # Add timeline
                timeline = self.sprint_manager.get_sprint_timeline(sprint_id)
                
                # Combine all data
                full_data = {
                    "id": sprint_id,
                    "status": sprint_info["status"].value if hasattr(sprint_info["status"], "value") else sprint_info["status"],
                    "metadata": sprint_info["metadata"],
                    "path": str(sprint_info["path"]),
                    "files": files_content,
                    "timeline": timeline or [],
                }
                
                full_sprint_data.append(full_data)
        
        # Prepare export metadata
        export_metadata = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "total_sprints": len(all_sprints),
            "exported_sprints": len(full_sprint_data),
            "format": format_name,
            "filters": {
                "status": [s.value for s in filter_criteria.status] if filter_criteria and filter_criteria.status else None,
                "since": filter_criteria.since.isoformat() if filter_criteria and filter_criteria.since else None,
                "until": filter_criteria.until.isoformat() if filter_criteria and filter_criteria.until else None,
                "author": filter_criteria.author if filter_criteria else None,
                "priority": filter_criteria.priority if filter_criteria else None,
                "tags": filter_criteria.tags if filter_criteria else None,
                "agents": filter_criteria.agents if filter_criteria else None,
            }
        }
        
        # Format data
        output = formatter.format(full_sprint_data, export_metadata)
        
        # Write to file if path provided
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(output, encoding="utf-8")
        
        return output
    
    def get_available_formats(self) -> List[str]:
        """Get list of registered format names."""
        return list(self.formatters.keys())
