"""
JSON export formatter for Stride sprint data.

Exports complete sprint data in JSON format with full metadata,
file contents, timeline events, and validation results.
"""

import json
from typing import Any, Dict, List

from stride.export.export_engine import ExportFormatter


class JSONFormatter(ExportFormatter):
    """JSON export formatter."""
    
    def __init__(self, indent: int = 2, compact: bool = False):
        """
        Initialize JSON formatter.
        
        Args:
            indent: Indentation level (default: 2)
            compact: If True, use compact output without indentation
        """
        self.indent = None if compact else indent
        self.compact = compact
    
    def format(self, sprints: List[Dict[str, Any]], metadata: Dict[str, Any]) -> str:
        """
        Format sprint data as JSON.
        
        Args:
            sprints: List of sprint data dictionaries
            metadata: Export metadata
            
        Returns:
            JSON-formatted string
        """
        output = {
            "export_metadata": metadata,
            "sprints": sprints
        }
        
        if self.compact:
            return json.dumps(output, separators=(',', ':'))
        else:
            return json.dumps(output, indent=self.indent, ensure_ascii=False)
    
    def get_extension(self) -> str:
        """Get file extension for JSON format."""
        return "json"
