"""
Pydantic data models for Stride entities.
"""

from datetime import datetime
from typing import List, Optional, Tuple, Dict, Any
from pathlib import Path
from dataclasses import dataclass, field
from pydantic import BaseModel, Field
from .constants import SprintStatus


class CheckboxItem(BaseModel):
    """Model representing a checkbox item from markdown."""
    text: str
    checked: bool
    line_number: int = 0


class StrideTask(BaseModel):
    """Model representing a stride milestone with tasks."""
    stride_number: int
    stride_name: str
    purpose: str = ""
    tasks: List[CheckboxItem] = Field(default_factory=list)
    completion_definition: str = ""
    
    @property
    def completed_tasks(self) -> int:
        """Count of completed tasks."""
        return sum(1 for task in self.tasks if task.checked)
    
    @property
    def total_tasks(self) -> int:
        """Total number of tasks."""
        return len(self.tasks)
    
    @property
    def completion_percentage(self) -> float:
        """Percentage of tasks completed."""
        if self.total_tasks == 0:
            return 0.0
        return (self.completed_tasks / self.total_tasks) * 100


class SprintProgress(BaseModel):
    """Model representing overall sprint progress."""
    total_tasks: int = 0
    completed_tasks: int = 0
    completion_percentage: float = 0.0
    strides: List[StrideTask] = Field(default_factory=list)
    acceptance_criteria_total: int = 0
    acceptance_criteria_completed: int = 0
    acceptance_criteria_percentage: float = 0.0
    
    @property
    def current_stride(self) -> Optional[StrideTask]:
        """Get the current stride being worked on (first incomplete stride)."""
        for stride in self.strides:
            if stride.completed_tasks < stride.total_tasks:
                return stride
        return None


class ImplementationLogEntry(BaseModel):
    """Model representing an implementation log entry."""
    timestamp: str
    stride_name: str
    tasks_addressed: List[str] = Field(default_factory=list)
    decisions: List[str] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)
    changes: List[str] = Field(default_factory=list)


class Sprint(BaseModel):
    """Model representing a single sprint."""
    id: str
    title: str
    status: SprintStatus
    path: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    progress: Optional[SprintProgress] = None
    acceptance_criteria: List[CheckboxItem] = Field(default_factory=list)
    recent_logs: List[ImplementationLogEntry] = Field(default_factory=list)


class Project(BaseModel):
    """Model representing the Stride project configuration."""
    name: str
    version: str = "0.1.0"


@dataclass
class SprintData:
    """Data class for sprint analytics."""
    sprint_id: str
    title: str
    description: str
    status: str
    created_date: datetime
    completed_date: Optional[datetime]
    duration_days: Optional[float]
    
    # Task data
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    task_completion_rate: float
    
    # Process compliance
    has_planning: bool
    has_implementation: bool
    has_retrospective: bool
    has_design: bool
    has_proposal: bool
    
    # Quality indicators
    retrospective_length: int
    learnings_count: int
    
    # Metadata
    folder_path: Path
    files_present: List[str]
    
    @property
    def is_completed(self) -> bool:
        """Check if sprint is completed."""
        return self.status.lower() == "completed"
    
    @property
    def is_active(self) -> bool:
        """Check if sprint is active."""
        return self.status.lower() == "active"
    
    @property
    def process_compliance_score(self) -> float:
        """Calculate process compliance (0-100)."""
        checks = [
            self.has_planning,
            self.has_implementation,
            self.has_retrospective,
        ]
        return (sum(checks) / len(checks)) * 100


@dataclass
class NiceBlock:
    intent_type: str          # ENTRY, FLOW, LOGIC, TRANSFORM, IO, etc.
    id: str                   # Human-readable identifier
    uid: str                  # nice:{type}:{domain}:{id}:v{N}
    file_path: str            # Absolute path to source file
    line_range: Tuple[int, int]  # Start and end line numbers
    tags: Dict[str, Any]      # All extracted tags (@desc, @inputs, etc.)
    semantic_hash: str        # Hash of semantic content (for drift detection)

@dataclass
class NiceManifest:
    blocks: List[NiceBlock]   # All parsed blocks
    timestamp: str            # When manifest was generated
    project_context: str      # Project root path
    total_files: int          # Files scanned
    coverage_stats: Dict      # Coverage by file/directory

@dataclass
class MarkerValidationResult:
    is_valid: bool
    errors: List[str]         # Blocking issues (missing required tags)
    warnings: List[str]       # Non-blocking issues (missing recommended tags)
    suggestions: List[str]    # Optimization suggestions

@dataclass
class Subtask:
    description: str
    completed: bool = False

@dataclass
class CategoryResult:
    passed: int
    failed: int
    warnings: int
    items: List[str]

@dataclass
class GeneratedTest:
    name: str
    file_path: str
    status: str

@dataclass
class ValidationReport:
    overall_status: str       # PASS, FAIL
    duration: str
    categories: Dict[str, CategoryResult]
    generated_tests: List[GeneratedTest]
    mutation_score: Optional[float]
    recommendations: List[str]

@dataclass
class LearningEntry:
    category: str             # Domain Knowledge, Technical Patterns, etc.
    subcategory: str          # Auth, Database, API Design, etc.
    content: str              # The actual learning
    context: str              # Why it matters
    sprint_id: str            # Sprint that discovered this
    is_antipattern: bool      # True if this is what NOT to do
    timestamp: str
    pattern_code: Optional[str] = None  # Example code snippet
