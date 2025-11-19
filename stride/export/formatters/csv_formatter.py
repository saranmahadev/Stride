"""
CSV export formatter for Stride sprint data.

Exports sprint data as CSV files suitable for spreadsheets and data analysis.
Creates a main sprint metadata CSV with optional separate files for tasks and timeline.
"""

import csv
import io
from typing import Any, Dict, List

from stride.export.export_engine import ExportFormatter


class CSVFormatter(ExportFormatter):
    """CSV export formatter."""
    
    def __init__(self, include_timeline: bool = False, include_tasks: bool = False):
        """
        Initialize CSV formatter.
        
        Args:
            include_timeline: If True, include timeline events in output
            include_tasks: If True, extract and include tasks from proposal
        """
        self.include_timeline = include_timeline
        self.include_tasks = include_tasks
    
    def format(self, sprints: List[Dict[str, Any]], metadata: Dict[str, Any]) -> str:
        """
        Format sprint data as CSV.
        
        Args:
            sprints: List of sprint data dictionaries
            metadata: Export metadata
            
        Returns:
            CSV-formatted string
        """
        output = io.StringIO()
        
        # Write metadata header
        output.write(f"# Sprint Export Report\n")
        output.write(f"# Generated: {metadata['timestamp']}\n")
        output.write(f"# Total Sprints: {metadata['total_sprints']}\n")
        output.write(f"# Exported Sprints: {metadata['exported_sprints']}\n")
        output.write(f"#\n")
        
        # Write main sprint data
        if sprints:
            fieldnames = [
                "sprint_id",
                "status",
                "title",
                "author",
                "priority",
                "created",
                "updated",
                "tags",
                "agents",
                "description",
                "has_proposal",
                "has_plan",
                "has_design",
                "has_implementation",
                "has_retrospective",
                "event_count",
            ]
            
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            
            for sprint in sprints:
                sprint_id = sprint["id"]
                sprint_metadata = sprint["metadata"]
                files = sprint.get("files", {})
                timeline = sprint.get("timeline", [])
                
                row = {
                    "sprint_id": sprint_id,
                    "status": sprint["status"],
                    "title": sprint_metadata.get("title", ""),
                    "author": sprint_metadata.get("author", ""),
                    "priority": sprint_metadata.get("priority", ""),
                    "created": sprint_metadata.get("created", ""),
                    "updated": sprint_metadata.get("updated", ""),
                    "tags": ";".join(sprint_metadata.get("tags", [])),
                    "agents": ";".join(sprint_metadata.get("agents", [])),
                    "description": sprint_metadata.get("description", "").replace("\n", " "),
                    "has_proposal": "yes" if files.get("proposal.md") else "no",
                    "has_plan": "yes" if files.get("plan.md") else "no",
                    "has_design": "yes" if files.get("design.md") else "no",
                    "has_implementation": "yes" if files.get("implementation.md") else "no",
                    "has_retrospective": "yes" if files.get("retrospective.md") else "no",
                    "event_count": len(timeline),
                }
                
                writer.writerow(row)
        else:
            output.write("# No sprints match the filter criteria.\n")
        
        return output.getvalue()
    
    def get_extension(self) -> str:
        """Get file extension for CSV format."""
        return "csv"
