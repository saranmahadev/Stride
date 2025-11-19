"""
Enhanced validators for sprint quality checks.

Provides comprehensive validation including:
- Structure validation (files, folders)
- Content quality checks (completeness, formatting)
- Metadata validation (required fields, consistency)
- Optional code quality checks (linting, testing)
"""
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
import re
import logging

logger = logging.getLogger(__name__)


class ValidationResult:
    """Container for validation results."""
    
    def __init__(self, category: str):
        self.category = category
        self.passed: List[str] = []
        self.warnings: List[str] = []
        self.errors: List[str] = []
        self.suggestions: List[str] = []
    
    def add_pass(self, message: str):
        """Add a passed check."""
        self.passed.append(message)
    
    def add_warning(self, message: str):
        """Add a warning."""
        self.warnings.append(message)
    
    def add_error(self, message: str):
        """Add an error."""
        self.errors.append(message)
    
    def add_suggestion(self, message: str):
        """Add a suggestion."""
        self.suggestions.append(message)
    
    @property
    def is_valid(self) -> bool:
        """Check if validation passed (no errors)."""
        return len(self.errors) == 0
    
    @property
    def total_checks(self) -> int:
        """Total number of checks performed."""
        return len(self.passed) + len(self.warnings) + len(self.errors)


class SprintValidator:
    """Enhanced sprint validator with quality checks."""
    
    # Minimum content lengths for quality checks
    MIN_PROPOSAL_LENGTH = 100  # characters
    MIN_PLAN_LENGTH = 50
    MIN_DESIGN_LENGTH = 50
    
    # Expected sections in documents
    PROPOSAL_SECTIONS = ["objective", "scope", "requirements"]
    PLAN_SECTIONS = ["tasks", "timeline", "deliverables"]
    DESIGN_SECTIONS = ["architecture", "components", "dependencies"]
    
    def __init__(self, sprint_path: Path, metadata: Dict[str, Any]):
        """
        Initialize validator.
        
        Args:
            sprint_path: Path to sprint folder
            metadata: Parsed metadata from proposal.md
        """
        self.sprint_path = sprint_path
        self.metadata = metadata
        self.results: Dict[str, ValidationResult] = {}
    
    def validate_structure(self) -> ValidationResult:
        """Validate sprint folder structure."""
        result = ValidationResult("Structure")
        
        # Check required files
        proposal_file = self.sprint_path / "proposal.md"
        if proposal_file.exists():
            result.add_pass("proposal.md exists")
        else:
            result.add_error("Missing proposal.md")
        
        # Check optional files
        optional_files = ["plan.md", "design.md", "implementation.md", "retrospective.md"]
        for filename in optional_files:
            file_path = self.sprint_path / filename
            if file_path.exists():
                result.add_pass(f"{filename} exists")
            else:
                result.add_warning(f"{filename} not found (optional)")
        
        # Check for unexpected files
        expected_files = {"proposal.md", "plan.md", "design.md", "implementation.md", "retrospective.md", ".history"}
        actual_files = {f.name for f in self.sprint_path.iterdir()}
        unexpected = actual_files - expected_files
        
        if unexpected:
            for filename in unexpected:
                if not filename.startswith('.'):  # Ignore hidden files
                    result.add_warning(f"Unexpected file: {filename}")
        
        self.results["structure"] = result
        return result
    
    def validate_content_quality(self) -> ValidationResult:
        """Validate content quality and completeness."""
        result = ValidationResult("Content Quality")
        
        # Check proposal.md content
        proposal_file = self.sprint_path / "proposal.md"
        if proposal_file.exists():
            content = proposal_file.read_text(encoding="utf-8")
            # Strip frontmatter for content analysis
            body = self._extract_body(content)
            
            if len(body) < self.MIN_PROPOSAL_LENGTH:
                result.add_warning(
                    f"Proposal is very short ({len(body)} chars, recommended: {self.MIN_PROPOSAL_LENGTH}+)"
                )
            else:
                result.add_pass(f"Proposal has adequate content ({len(body)} chars)")
            
            # Check for key sections
            body_lower = body.lower()
            for section in self.PROPOSAL_SECTIONS:
                if section in body_lower or f"# {section}" in body_lower or f"## {section}" in body_lower:
                    result.add_pass(f"Contains '{section}' section")
                else:
                    result.add_suggestion(f"Consider adding '{section}' section")
            
            # Check for code blocks (should have examples or specs)
            if "```" in body:
                result.add_pass("Contains code examples or specifications")
            else:
                result.add_suggestion("Consider adding code examples or technical specifications")
        
        # Check plan.md if it exists
        plan_file = self.sprint_path / "plan.md"
        if plan_file.exists():
            content = plan_file.read_text(encoding="utf-8")
            body = self._extract_body(content)
            
            if len(body) < self.MIN_PLAN_LENGTH:
                result.add_warning(f"Plan is very short ({len(body)} chars)")
            else:
                result.add_pass(f"Plan has adequate content ({len(body)} chars)")
            
            # Check for tasks/checkboxes
            checkboxes = re.findall(r'[-*]\s*\[[x ]\]', content, re.IGNORECASE)
            if checkboxes:
                result.add_pass(f"Contains {len(checkboxes)} task checkboxes")
            else:
                result.add_suggestion("Consider adding task checkboxes for tracking")
        
        # Check design.md if it exists
        design_file = self.sprint_path / "design.md"
        if design_file.exists():
            content = design_file.read_text(encoding="utf-8")
            body = self._extract_body(content)
            
            if len(body) >= self.MIN_DESIGN_LENGTH:
                result.add_pass(f"Design document exists ({len(body)} chars)")
            else:
                result.add_warning("Design document is very short")
        
        self.results["content_quality"] = result
        return result
    
    def validate_metadata_completeness(self) -> ValidationResult:
        """Validate metadata completeness and consistency."""
        result = ValidationResult("Metadata")
        
        # Check required fields
        required_fields = ["id", "title", "status", "created"]
        for field in required_fields:
            if field in self.metadata and self.metadata[field]:
                result.add_pass(f"Required field '{field}' present")
            else:
                result.add_error(f"Missing required field: {field}")
        
        # Check optional but recommended fields
        recommended_fields = ["author", "priority", "tags"]
        for field in recommended_fields:
            if field in self.metadata and self.metadata[field]:
                result.add_pass(f"Recommended field '{field}' present")
            else:
                result.add_warning(f"Missing recommended field: {field}")
        
        # Validate field content
        if "title" in self.metadata:
            title = self.metadata["title"]
            if len(title) < 10:
                result.add_warning("Title is very short (< 10 chars)")
            elif len(title) > 100:
                result.add_warning("Title is very long (> 100 chars)")
            else:
                result.add_pass("Title has reasonable length")
        
        if "tags" in self.metadata:
            tags = self.metadata["tags"]
            if isinstance(tags, list):
                if len(tags) == 0:
                    result.add_warning("Tags field is empty")
                elif len(tags) > 10:
                    result.add_warning(f"Many tags ({len(tags)}), consider reducing")
                else:
                    result.add_pass(f"Has {len(tags)} tag(s)")
        
        if "priority" in self.metadata:
            priority = self.metadata["priority"]
            valid_priorities = ["low", "medium", "high", "critical"]
            if priority in valid_priorities:
                result.add_pass(f"Valid priority: {priority}")
            else:
                result.add_warning(f"Unusual priority value: {priority}")
        
        self.results["metadata"] = result
        return result
    
    def validate_consistency(self) -> ValidationResult:
        """Validate consistency across documents."""
        result = ValidationResult("Consistency")
        
        # Check sprint ID consistency
        sprint_id = self.metadata.get("id", "")
        if sprint_id:
            folder_name = self.sprint_path.name
            if sprint_id == folder_name:
                result.add_pass("Sprint ID matches folder name")
            else:
                result.add_error(f"Sprint ID mismatch: metadata={sprint_id}, folder={folder_name}")
        
        # Check if created timestamp is valid
        if "created" in self.metadata:
            created = self.metadata["created"]
            if isinstance(created, str) and len(created) > 0:
                result.add_pass("Created timestamp present")
            else:
                result.add_error("Invalid created timestamp")
        
        # Check updated vs created
        if "created" in self.metadata and "updated" in self.metadata:
            result.add_pass("Both created and updated timestamps present")
        elif "updated" in self.metadata:
            result.add_warning("Has updated but missing created timestamp")
        
        self.results["consistency"] = result
        return result
    
    def validate_all(self) -> Dict[str, ValidationResult]:
        """
        Run all validations.
        
        Returns:
            Dictionary of validation results by category
        """
        self.validate_structure()
        self.validate_content_quality()
        self.validate_metadata_completeness()
        self.validate_consistency()
        
        return self.results
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get validation summary.
        
        Returns:
            Dictionary with summary statistics
        """
        total_checks = sum(r.total_checks for r in self.results.values())
        total_passed = sum(len(r.passed) for r in self.results.values())
        total_warnings = sum(len(r.warnings) for r in self.results.values())
        total_errors = sum(len(r.errors) for r in self.results.values())
        total_suggestions = sum(len(r.suggestions) for r in self.results.values())
        
        is_valid = all(r.is_valid for r in self.results.values())
        
        return {
            "is_valid": is_valid,
            "total_checks": total_checks,
            "passed": total_passed,
            "warnings": total_warnings,
            "errors": total_errors,
            "suggestions": total_suggestions,
            "categories": {
                name: {
                    "passed": len(r.passed),
                    "warnings": len(r.warnings),
                    "errors": len(r.errors),
                    "suggestions": len(r.suggestions),
                    "is_valid": r.is_valid
                }
                for name, r in self.results.items()
            }
        }
    
    @staticmethod
    def _extract_body(content: str) -> str:
        """
        Extract body content from markdown, removing frontmatter.
        
        Args:
            content: Full markdown content
            
        Returns:
            Body content without frontmatter
        """
        # Remove YAML frontmatter if present
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                return parts[2].strip()
        return content.strip()
