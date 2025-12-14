"""
Approval workflow management for sprint completion.

This module provides functions for managing sprint approvals, checking
approval thresholds, and tracking approval history.
"""

from pathlib import Path
from typing import Optional, List, Dict, Tuple
from datetime import datetime

from stride.models import SprintMetadata, TeamConfig, Approval
from stride.core.team_file_manager import (
    read_team_config,
    read_sprint_metadata,
    write_sprint_metadata
)
from stride.utils import get_stride_dir


def can_approve(
    approver_email: str,
    team_config: Optional[TeamConfig] = None
) -> Tuple[bool, Optional[str]]:
    """
    Check if a team member has permission to approve sprints.
    
    Args:
        approver_email: Email of potential approver
        team_config: TeamConfig object (reads from file if None)
    
    Returns:
        Tuple of (can_approve: bool, reason: Optional[str])
        reason is None if can approve, otherwise contains explanation
    
    Raises:
        FileNotFoundError: If team.yaml doesn't exist
    """
    if team_config is None:
        team_config = read_team_config()
    
    # Check if approval workflow is enabled
    policy = team_config.approval_policy
    if not policy.get("enabled", True):
        return (False, "Approval workflow is disabled")
    
    # Check if member exists
    member = team_config.get_member(approver_email)
    if not member:
        return (False, f"Member '{approver_email}' not found in team.yaml")
    
    # Check if member has approval permissions
    roles_can_approve = policy.get("roles_can_approve", ["lead", "reviewer"])
    member_roles = set(member.roles.keys())
    
    if not any(role in roles_can_approve for role in member_roles):
        return (False, f"Role required: {', '.join(roles_can_approve)}")
    
    return (True, None)


def approve_sprint(
    sprint_id: str,
    approver_email: str,
    comment: Optional[str] = None
) -> SprintMetadata:
    """
    Add approval to a sprint.
    
    Args:
        sprint_id: Sprint identifier
        approver_email: Email of approver
        comment: Optional approval comment
    
    Returns:
        Updated SprintMetadata object
    
    Raises:
        FileNotFoundError: If sprint directory or team.yaml doesn't exist
        ValueError: If approver doesn't have permission
        ValueError: If approver already approved
    """
    # Validate approver permissions
    team_config = read_team_config()
    can_approve_result, reason = can_approve(approver_email, team_config)
    if not can_approve_result:
        raise ValueError(f"Cannot approve: {reason}")
    
    # Check sprint exists
    stride_dir = get_stride_dir()
    sprint_dir = stride_dir / "sprints" / sprint_id
    if not sprint_dir.exists():
        raise FileNotFoundError(f"Sprint directory not found: {sprint_dir}")
    
    # Read existing metadata or create new
    metadata = read_sprint_metadata(sprint_id)
    if metadata is None:
        metadata = SprintMetadata(
            assigned_to=None,
            assigned_by=None,
            assigned_at=None,
            approvals=[],
            history=[]
        )
    
    # Check if already approved by this person
    if metadata.has_approved(approver_email):
        raise ValueError(
            f"Sprint already approved by {approver_email}"
        )
    
    # Create approval
    approval = Approval(
        approver=approver_email,
        approved_at=datetime.now(),
        comment=comment
    )
    
    # Add approval
    metadata.approvals.append(approval)
    
    # Add history event
    member = team_config.get_member(approver_email)
    metadata.history.append({
        "event": "approved",
        "timestamp": datetime.now(),
        "actor": approver_email,
        "details": {
            "approver_name": member.name if member else approver_email,
            "comment": comment,
            "approval_count": len(metadata.approvals)
        }
    })
    
    # Write metadata
    write_sprint_metadata(sprint_id, metadata)
    
    return metadata


def revoke_approval(
    sprint_id: str,
    approver_email: str
) -> SprintMetadata:
    """
    Revoke an approval from a sprint.
    
    Args:
        sprint_id: Sprint identifier
        approver_email: Email of approver whose approval to revoke
    
    Returns:
        Updated SprintMetadata object
    
    Raises:
        FileNotFoundError: If sprint directory doesn't exist
        ValueError: If no approval exists from this approver
    """
    # Check sprint exists
    stride_dir = get_stride_dir()
    sprint_dir = stride_dir / "sprints" / sprint_id
    if not sprint_dir.exists():
        raise FileNotFoundError(f"Sprint directory not found: {sprint_dir}")
    
    # Read metadata
    metadata = read_sprint_metadata(sprint_id)
    if metadata is None:
        raise ValueError(f"No metadata found for sprint {sprint_id}")
    
    # Find and remove approval
    original_count = len(metadata.approvals)
    metadata.approvals = [
        a for a in metadata.approvals
        if a.approver != approver_email
    ]
    
    if len(metadata.approvals) == original_count:
        raise ValueError(
            f"No approval found from {approver_email} for sprint {sprint_id}"
        )
    
    # Add history event
    metadata.history.append({
        "event": "approval_revoked",
        "timestamp": datetime.now(),
        "actor": approver_email,
        "details": {"approval_count": len(metadata.approvals)}
    })
    
    # Write metadata
    write_sprint_metadata(sprint_id, metadata)
    
    return metadata


def get_approval_status(
    sprint_id: str,
    team_config: Optional[TeamConfig] = None
) -> Dict[str, any]:
    """
    Get comprehensive approval status for a sprint.
    
    Args:
        sprint_id: Sprint identifier
        team_config: TeamConfig object (reads from file if None)
    
    Returns:
        Dict with current_approvals, required_approvals, approved,
        approvers, can_complete, missing_approvals
    
    Raises:
        FileNotFoundError: If sprint directory doesn't exist
    """
    if team_config is None:
        try:
            team_config = read_team_config()
        except FileNotFoundError:
            # No team config, approvals not applicable
            return {
                "workflow_enabled": False,
                "current_approvals": 0,
                "required_approvals": 0,
                "approved": True,
                "approvers": [],
                "can_complete": True,
                "missing_approvals": 0
            }
    
    # Check sprint exists
    stride_dir = get_stride_dir()
    sprint_dir = stride_dir / "sprints" / sprint_id
    if not sprint_dir.exists():
        raise FileNotFoundError(f"Sprint directory not found: {sprint_dir}")
    
    # Get approval policy
    policy = team_config.approval_policy
    workflow_enabled = policy.get("enabled", True)
    required_approvals = policy.get("required_approvals", 1)
    
    # Read metadata
    metadata = read_sprint_metadata(sprint_id)
    current_approvals = metadata.approval_count if metadata else 0
    approvers = []
    
    if metadata:
        for approval in metadata.approvals:
            member = team_config.get_member(approval.approver)
            approvers.append({
                "email": approval.approver,
                "name": member.name if member else approval.approver,
                "approved_at": approval.approved_at,
                "comment": approval.comment
            })
    
    # Calculate status
    approved = current_approvals >= required_approvals
    missing_approvals = max(0, required_approvals - current_approvals)
    can_complete = approved or not workflow_enabled
    
    return {
        "workflow_enabled": workflow_enabled,
        "current_approvals": current_approvals,
        "required_approvals": required_approvals,
        "approved": approved,
        "approvers": approvers,
        "can_complete": can_complete,
        "missing_approvals": missing_approvals
    }


def get_pending_approvals(
    approver_email: Optional[str] = None
) -> List[Dict[str, any]]:
    """
    Get list of sprints pending approval.
    
    Args:
        approver_email: Filter to sprints where this person can approve
                       (None returns all pending sprints)
    
    Returns:
        List of dicts with sprint_id, assignee, current_approvals,
        required_approvals, missing_approvals
    
    Raises:
        FileNotFoundError: If .stride directory doesn't exist
    """
    stride_dir = get_stride_dir()
    sprints_dir = stride_dir / "sprints"
    
    if not sprints_dir.exists():
        return []
    
    # Load team config
    try:
        team_config = read_team_config()
        policy = team_config.approval_policy
        workflow_enabled = policy.get("enabled", True)
        required_approvals = policy.get("required_approvals", 1)
    except FileNotFoundError:
        # No team config, no pending approvals
        return []
    
    if not workflow_enabled:
        return []
    
    # Check approver permissions if specified
    if approver_email:
        can_approve_result, _ = can_approve(approver_email, team_config)
        if not can_approve_result:
            return []
    
    pending = []
    
    for sprint_dir in sprints_dir.iterdir():
        if not sprint_dir.is_dir():
            continue
        
        sprint_id = sprint_dir.name
        metadata = read_sprint_metadata(sprint_id)
        
        # Skip if no metadata or already fully approved
        if metadata is None:
            continue
        
        current_approvals = metadata.approval_count
        if current_approvals >= required_approvals:
            continue
        
        # If filtering by approver, skip if already approved by them
        if approver_email and metadata.has_approved(approver_email):
            continue
        
        pending.append({
            "sprint_id": sprint_id,
            "assignee": metadata.assigned_to,
            "current_approvals": current_approvals,
            "required_approvals": required_approvals,
            "missing_approvals": required_approvals - current_approvals,
            "approvers": [a.approver for a in metadata.approvals]
        })
    
    # Sort by assignment date (most recent first)
    pending.sort(
        key=lambda x: x.get("assigned_at", datetime.min),
        reverse=True
    )
    
    return pending
