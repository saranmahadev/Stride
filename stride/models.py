"""
Pydantic data models for Stride entities.
"""

from datetime import datetime
from typing import List, Optional, Dict
from pathlib import Path
from dataclasses import dataclass
from pydantic import BaseModel, Field, EmailStr
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


# ============================================================================
# Team Collaboration Models (v1.5)
# ============================================================================


class TeamMember(BaseModel):
    """
    Model representing a team member.
    
    Attributes:
        username: Unique identifier (3-30 chars, alphanumeric + dash)
        email: Valid email address
        role: One of ["admin", "developer", "reviewer", "viewer"]
        joined_at: Timestamp when member joined
        active: Whether member is currently active
    """
    username: str = Field(..., min_length=3, max_length=30, pattern=r"^[a-z0-9\-]+$")
    email: EmailStr
    role: str = Field(..., pattern=r"^(admin|developer|reviewer|viewer)$")
    joined_at: datetime = Field(default_factory=datetime.now)
    active: bool = True


class ApprovalPolicy(BaseModel):
    """
    Model representing approval workflow policy.
    
    Attributes:
        required_approvers: Number of approvals required (0 = no approvals)
        allow_self_approval: Whether sprint assignee can approve their own work
        block_completion: Whether to block completion without sufficient approvals
    """
    required_approvers: int = Field(default=0, ge=0)
    allow_self_approval: bool = False
    block_completion: bool = True


class TeamConfig(BaseModel):
    """
    Model representing team configuration stored in .stride/team.yaml.
    
    Attributes:
        schema_version: Schema version for future migrations
        project_name: Project name from project.md
        created_at: Team initialization timestamp
        members: List of team members
        roles: Role definitions with permissions
        approval_policy: Approval workflow configuration
    """
    schema_version: str = "1.5"
    project_name: str = Field(..., min_length=3, max_length=100)
    created_at: datetime = Field(default_factory=datetime.now)
    members: List[TeamMember] = Field(default_factory=list)
    roles: Dict[str, List[str]] = Field(default_factory=dict)
    approval_policy: ApprovalPolicy = Field(default_factory=ApprovalPolicy)
    
    def get_member(self, username: str) -> Optional[TeamMember]:
        """Get team member by username."""
        for member in self.members:
            if member.username == username:
                return member
        return None
    
    def has_member(self, username: str) -> bool:
        """Check if username exists in team."""
        return self.get_member(username) is not None


class Approval(BaseModel):
    """
    Model representing a single approval.
    
    Attributes:
        approver: Username of approver
        approved_at: Timestamp of approval
    """
    approver: str
    approved_at: datetime = Field(default_factory=datetime.now)


class MetadataEvent(BaseModel):
    """
    Model representing a metadata history event.
    
    Attributes:
        event: Event type (assigned, approved, unassigned, etc.)
        user: Username who triggered the event
        timestamp: When the event occurred
        details: Optional additional details
    """
    event: str
    user: str
    timestamp: datetime = Field(default_factory=datetime.now)
    details: Optional[str] = None


class SprintMetadata(BaseModel):
    """
    Model representing sprint ownership and approval tracking.
    Stored in .stride/sprints/<ID>/.metadata.yaml.
    
    Attributes:
        sprint_id: Sprint identifier
        assignee: Assigned team member username
        created_at: Sprint creation timestamp
        assigned_at: Assignment timestamp
        status: Sprint status (proposed, active, completed)
        approvals: List of approval records
        tags: Optional tags for filtering
        history: Assignment/approval history
    """
    sprint_id: str
    assignee: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    assigned_at: Optional[datetime] = None
    status: str = "proposed"
    approvals: List[Approval] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    history: List[MetadataEvent] = Field(default_factory=list)
    
    @property
    def approval_count(self) -> int:
        """Get number of approvals."""
        return len(self.approvals)
    
    def has_approved(self, username: str) -> bool:
        """Check if user has already approved."""
        return any(approval.approver == username for approval in self.approvals)


class Comment(BaseModel):
    """
    Model representing a threaded comment.
    Stored in .stride/sprints/<ID>/.comments.yaml.
    
    Attributes:
        id: Unique comment ID (e.g., "C1", "C2", "C1.1" for replies)
        author: Username from team.yaml
        timestamp: Comment creation time
        message: Comment text (1-5000 chars)
        file_path: Optional file anchor (relative path)
        line_number: Optional line anchor (positive int)
        status: One of ["open", "resolved"]
        replies: Nested replies (recursive structure)
    """
    id: str
    author: str
    timestamp: datetime = Field(default_factory=datetime.now)
    message: str = Field(..., min_length=1, max_length=5000)
    file_path: Optional[str] = None
    line_number: Optional[int] = Field(None, gt=0)
    status: str = Field(default="open", pattern=r"^(open|resolved)$")
    replies: List['Comment'] = Field(default_factory=list)
    
    @property
    def has_replies(self) -> bool:
        """Check if comment has replies."""
        return len(self.replies) > 0
    
    @property
    def is_resolved(self) -> bool:
        """Check if comment is resolved."""
        return self.status == "resolved"


# Enable forward reference resolution for recursive Comment model
Comment.model_rebuild()
