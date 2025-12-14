"""
Sprint assignment management for team collaboration.

This module provides functions for assigning sprints to team members,
tracking assignments, and providing AI-powered assignment recommendations.
"""

from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime

from stride.models import SprintMetadata, TeamConfig, TeamMember
from stride.core.team_file_manager import (
    read_team_config,
    read_sprint_metadata,
    write_sprint_metadata
)
from stride.utils import get_stride_dir


def assign_sprint(
    sprint_id: str,
    assignee_email: str,
    assigner_email: Optional[str] = None
) -> SprintMetadata:
    """
    Assign a sprint to a team member.
    
    Creates or updates the .metadata.yaml file in the sprint directory with
    the assignment information.
    
    Args:
        sprint_id: Sprint identifier (e.g., 'sprint-feature-name')
        assignee_email: Email of the team member to assign the sprint to
        assigner_email: Email of the person making the assignment (optional)
    
    Returns:
        Updated SprintMetadata object
    
    Raises:
        FileNotFoundError: If sprint directory or team.yaml doesn't exist
        ValueError: If assignee email is not in team.yaml
    """
    # Validate team member exists
    team_config = read_team_config()
    assignee = team_config.get_member(assignee_email)
    if not assignee:
        raise ValueError(
            f"Assignee '{assignee_email}' not found in team.yaml. "
            f"Add them with: stride team add"
        )
    
    # Validate assigner if provided
    if assigner_email:
        assigner = team_config.get_member(assigner_email)
        if not assigner:
            raise ValueError(
                f"Assigner '{assigner_email}' not found in team.yaml"
            )
    
    # Check sprint exists
    stride_dir = get_stride_dir()
    sprint_dir = stride_dir / "sprints" / sprint_id
    if not sprint_dir.exists():
        raise FileNotFoundError(
            f"Sprint directory not found: {sprint_dir}\n"
            f"Available sprints: stride list"
        )
    
    # Read existing metadata or create new
    metadata = read_sprint_metadata(sprint_id)
    if metadata is None:
        metadata = SprintMetadata(
            assigned_to=assignee_email,
            assigned_by=assigner_email,
            assigned_at=datetime.now(),
            approvals=[],
            history=[]
        )
    else:
        # Update assignment
        metadata.assigned_to = assignee_email
        metadata.assigned_by = assigner_email
        metadata.assigned_at = datetime.now()
    
    # Add history event
    metadata.history.append({
        "event": "assigned",
        "timestamp": datetime.now(),
        "actor": assigner_email or "system",
        "details": {
            "assignee": assignee_email,
            "previous_assignee": metadata.assigned_to if metadata else None
        }
    })
    
    # Write metadata
    write_sprint_metadata(sprint_id, metadata)
    
    return metadata


def unassign_sprint(
    sprint_id: str,
    actor_email: Optional[str] = None
) -> Optional[SprintMetadata]:
    """
    Remove assignment from a sprint.
    
    Args:
        sprint_id: Sprint identifier
        actor_email: Email of the person removing the assignment (optional)
    
    Returns:
        Updated SprintMetadata object, or None if no metadata existed
    
    Raises:
        FileNotFoundError: If sprint directory doesn't exist
    """
    # Check sprint exists
    stride_dir = get_stride_dir()
    sprint_dir = stride_dir / "sprints" / sprint_id
    if not sprint_dir.exists():
        raise FileNotFoundError(f"Sprint directory not found: {sprint_dir}")
    
    # Read metadata
    metadata = read_sprint_metadata(sprint_id)
    if metadata is None:
        return None
    
    previous_assignee = metadata.assigned_to
    
    # Clear assignment
    metadata.assigned_to = None
    metadata.assigned_by = None
    metadata.assigned_at = None
    
    # Add history event
    metadata.history.append({
        "event": "unassigned",
        "timestamp": datetime.now(),
        "actor": actor_email or "system",
        "details": {"previous_assignee": previous_assignee}
    })
    
    # Write metadata
    write_sprint_metadata(sprint_id, metadata)
    
    return metadata


def get_assigned_sprints(
    assignee_email: Optional[str] = None,
    include_unassigned: bool = False
) -> List[Dict[str, any]]:
    """
    Get list of sprint assignments.
    
    Args:
        assignee_email: Filter by assignee email (None returns all)
        include_unassigned: Include sprints without assignments
    
    Returns:
        List of dicts with sprint_id, assignee, assigned_at, status
    
    Raises:
        FileNotFoundError: If .stride directory doesn't exist
    """
    stride_dir = get_stride_dir()
    sprints_dir = stride_dir / "sprints"
    
    if not sprints_dir.exists():
        return []
    
    assignments = []
    
    for sprint_dir in sprints_dir.iterdir():
        if not sprint_dir.is_dir():
            continue
        
        sprint_id = sprint_dir.name
        metadata = read_sprint_metadata(sprint_id)
        
        # Handle unassigned sprints
        if metadata is None or metadata.assigned_to is None:
            if include_unassigned:
                assignments.append({
                    "sprint_id": sprint_id,
                    "assignee": None,
                    "assigned_at": None,
                    "assigned_by": None,
                    "approval_count": 0,
                    "status": "unassigned"
                })
            continue
        
        # Filter by assignee if specified
        if assignee_email and metadata.assigned_to != assignee_email:
            continue
        
        # Determine status
        status = "assigned"
        if metadata.approval_count > 0:
            status = "in_review"
        
        assignments.append({
            "sprint_id": sprint_id,
            "assignee": metadata.assigned_to,
            "assigned_at": metadata.assigned_at,
            "assigned_by": metadata.assigned_by,
            "approval_count": metadata.approval_count,
            "status": status
        })
    
    # Sort by assigned_at (most recent first)
    assignments.sort(
        key=lambda x: x["assigned_at"] or datetime.min,
        reverse=True
    )
    
    return assignments


def get_member_assignments(assignee_email: str) -> Dict[str, any]:
    """
    Get comprehensive assignment summary for a team member.
    
    Args:
        assignee_email: Email of team member
    
    Returns:
        Dict with assigned_sprints, total_count, pending_count
    
    Raises:
        FileNotFoundError: If .stride directory doesn't exist
        ValueError: If email not in team.yaml
    """
    # Validate team member
    team_config = read_team_config()
    member = team_config.get_member(assignee_email)
    if not member:
        raise ValueError(f"Member '{assignee_email}' not found in team.yaml")
    
    # Get assignments
    assignments = get_assigned_sprints(assignee_email=assignee_email)
    
    # Calculate counts
    pending_count = sum(1 for a in assignments if a["status"] == "assigned")
    in_review_count = sum(1 for a in assignments if a["status"] == "in_review")
    
    return {
        "member": member,
        "assigned_sprints": assignments,
        "total_count": len(assignments),
        "pending_count": pending_count,
        "in_review_count": in_review_count
    }


def recommend_assignee(
    sprint_id: str,
    team_config: Optional[TeamConfig] = None
) -> List[Dict[str, any]]:
    """
    Recommend team members for sprint assignment using AI heuristics.
    
    Considers factors:
    - Current workload (number of assigned sprints)
    - Member roles
    - Assignment history
    
    Args:
        sprint_id: Sprint identifier
        team_config: TeamConfig object (reads from file if None)
    
    Returns:
        List of dicts with member, score, reason (sorted by score desc)
    
    Raises:
        FileNotFoundError: If sprint or team.yaml doesn't exist
    """
    if team_config is None:
        team_config = read_team_config()
    
    # Check sprint exists
    stride_dir = get_stride_dir()
    sprint_dir = stride_dir / "sprints" / sprint_id
    if not sprint_dir.exists():
        raise FileNotFoundError(f"Sprint directory not found: {sprint_dir}")
    
    # Get current assignments for workload calculation
    all_assignments = get_assigned_sprints()
    workload = {}
    for assignment in all_assignments:
        assignee = assignment["assignee"]
        if assignee:
            workload[assignee] = workload.get(assignee, 0) + 1
    
    # Calculate scores for each member
    recommendations = []
    
    for member in team_config.members:
        score = 100  # Base score
        reasons = []
        
        # Factor 1: Workload (lower is better)
        member_workload = workload.get(member.email, 0)
        if member_workload == 0:
            score += 30
            reasons.append("No current assignments")
        elif member_workload == 1:
            score += 10
            reasons.append("Light workload (1 sprint)")
        elif member_workload >= 3:
            score -= 20
            reasons.append(f"Heavy workload ({member_workload} sprints)")
        else:
            reasons.append(f"Moderate workload ({member_workload} sprints)")
        
        # Factor 2: Roles
        if "lead" in member.roles:
            score += 15
            reasons.append("Team lead")
        if "developer" in member.roles:
            score += 5
            reasons.append("Developer role")
        
        # Factor 3: Historical assignments
        member_assignments = [
            a for a in all_assignments
            if a["assignee"] == member.email
        ]
        if len(member_assignments) > 0:
            # Check if recently assigned
            latest = member_assignments[0]  # Already sorted by date
            days_since = (datetime.now() - (latest["assigned_at"] or datetime.now())).days
            if days_since < 7:
                score -= 10
                reasons.append("Recently assigned")
        
        recommendations.append({
            "member": member,
            "score": score,
            "reasons": reasons,
            "current_workload": member_workload
        })
    
    # Sort by score (descending)
    recommendations.sort(key=lambda x: x["score"], reverse=True)
    
    return recommendations
