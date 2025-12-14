"""
Workload analysis and balancing for team sprint assignments.

This module provides functions for calculating member workload, sprint complexity
scoring, and workload distribution analysis to help teams balance assignments.
"""

from pathlib import Path
from typing import Dict, List, Optional
from statistics import mean, stdev

from stride.core.assignment_manager import get_assigned_sprints, get_member_assignments
from stride.core.team_file_manager import read_team_config, read_sprint_metadata
from stride.utils import get_stride_dir


def calculate_sprint_complexity(sprint_id: str) -> int:
    """
    Calculate complexity score for a sprint based on stride count and task count.
    
    Analyzes plan.md to count strides and tasks, returning a weighted complexity score.
    
    Args:
        sprint_id: Sprint identifier
    
    Returns:
        Complexity score (0-100 scale)
    
    Raises:
        FileNotFoundError: If sprint directory or plan.md doesn't exist
    """
    stride_dir = get_stride_dir()
    sprint_dir = stride_dir / "sprints" / sprint_id
    
    if not sprint_dir.exists():
        raise FileNotFoundError(f"Sprint directory not found: {sprint_dir}")
    
    plan_file = sprint_dir / "plan.md"
    if not plan_file.exists():
        return 10  # Default minimal complexity
    
    # Parse plan.md to count strides and tasks
    content = plan_file.read_text(encoding='utf-8')
    
    # Count strides (lines starting with "### **Stride")
    stride_count = content.count("### **Stride")
    
    # Count tasks (lines starting with "- [ ] Task")
    task_count = content.count("- [ ] Task")
    
    # Calculate complexity score
    # Formula: (stride_count * 5) + (task_count * 1)
    # Normalized to 0-100 scale
    base_score = (stride_count * 5) + task_count
    
    # Normalize to 0-100 (assuming max realistic is ~150)
    complexity = min(100, int((base_score / 150) * 100))
    
    return max(10, complexity)  # Minimum 10


def calculate_member_workload(
    member_email: str,
    include_complexity: bool = True
) -> Dict[str, any]:
    """
    Calculate comprehensive workload for a team member.
    
    Args:
        member_email: Email of team member
        include_complexity: Include complexity-weighted scores
    
    Returns:
        Dict with active_count, pending_count, in_review_count, complexity_score,
        weighted_load, assigned_sprints
    
    Raises:
        FileNotFoundError: If .stride directory doesn't exist
        ValueError: If member not in team.yaml
    """
    # Get basic assignment counts
    summary = get_member_assignments(member_email)
    
    active_count = summary["total_count"]
    pending_count = summary["pending_count"]
    in_review_count = summary["in_review_count"]
    
    # Calculate complexity-weighted load
    complexity_score = 0
    if include_complexity and summary["assigned_sprints"]:
        for assignment in summary["assigned_sprints"]:
            try:
                sprint_complexity = calculate_sprint_complexity(
                    assignment["sprint_id"]
                )
                complexity_score += sprint_complexity
            except:
                # If can't calculate complexity, assume medium (50)
                complexity_score += 50
    
    # Weighted load = sum of sprint complexities
    weighted_load = complexity_score
    
    return {
        "member_email": member_email,
        "active_count": active_count,
        "pending_count": pending_count,
        "in_review_count": in_review_count,
        "complexity_score": complexity_score,
        "weighted_load": weighted_load,
        "assigned_sprints": summary["assigned_sprints"]
    }


def calculate_team_workload() -> List[Dict[str, any]]:
    """
    Calculate workload for all team members.
    
    Returns:
        List of workload dicts for each member, sorted by weighted_load desc
    
    Raises:
        FileNotFoundError: If team.yaml doesn't exist
    """
    team_config = read_team_config()
    
    workloads = []
    for member in team_config.members:
        try:
            workload = calculate_member_workload(member.email)
            workload["member_name"] = member.name
            workloads.append(workload)
        except Exception:
            # Skip members with errors
            continue
    
    # Sort by weighted load (highest first)
    workloads.sort(key=lambda x: x["weighted_load"], reverse=True)
    
    return workloads


def analyze_workload_distribution() -> Dict[str, any]:
    """
    Analyze team-wide workload distribution statistics.
    
    Returns:
        Dict with total_members, total_sprints, avg_load, min_load, max_load,
        std_dev, balance_score (0-100, higher is more balanced)
    
    Raises:
        FileNotFoundError: If team.yaml doesn't exist
    """
    workloads = calculate_team_workload()
    
    if not workloads:
        return {
            "total_members": 0,
            "total_sprints": 0,
            "avg_load": 0.0,
            "min_load": 0,
            "max_load": 0,
            "std_dev": 0.0,
            "balance_score": 100
        }
    
    loads = [w["weighted_load"] for w in workloads]
    total_sprints = sum(w["active_count"] for w in workloads)
    
    avg_load = mean(loads) if loads else 0.0
    min_load = min(loads) if loads else 0
    max_load = max(loads) if loads else 0
    std_dev_val = stdev(loads) if len(loads) > 1 else 0.0
    
    # Balance score: 100 - (std_dev as percentage of mean)
    # Higher score = more balanced distribution
    if avg_load > 0:
        balance_score = max(0, min(100, 100 - int((std_dev_val / avg_load) * 100)))
    else:
        balance_score = 100
    
    return {
        "total_members": len(workloads),
        "total_sprints": total_sprints,
        "avg_load": round(avg_load, 1),
        "min_load": min_load,
        "max_load": max_load,
        "std_dev": round(std_dev_val, 1),
        "balance_score": balance_score
    }


def identify_overloaded_members(threshold: float = 1.5) -> List[Dict[str, any]]:
    """
    Identify team members with workload above threshold.
    
    Args:
        threshold: Multiple of average load to consider overloaded (default 1.5x)
    
    Returns:
        List of overloaded members with their workload details
    
    Raises:
        FileNotFoundError: If team.yaml doesn't exist
    """
    workloads = calculate_team_workload()
    
    if not workloads:
        return []
    
    distribution = analyze_workload_distribution()
    avg_load = distribution["avg_load"]
    
    if avg_load == 0:
        return []
    
    overload_threshold = avg_load * threshold
    
    overloaded = [
        w for w in workloads
        if w["weighted_load"] > overload_threshold
    ]
    
    return overloaded


def identify_underutilized_members(threshold: float = 0.5) -> List[Dict[str, any]]:
    """
    Identify team members with workload below threshold.
    
    Args:
        threshold: Multiple of average load to consider underutilized (default 0.5x)
    
    Returns:
        List of underutilized members with their workload details
    
    Raises:
        FileNotFoundError: If team.yaml doesn't exist
    """
    workloads = calculate_team_workload()
    
    if not workloads:
        return []
    
    distribution = analyze_workload_distribution()
    avg_load = distribution["avg_load"]
    
    if avg_load == 0:
        return []
    
    underutil_threshold = avg_load * threshold
    
    underutilized = [
        w for w in workloads
        if w["weighted_load"] < underutil_threshold
    ]
    
    return underutilized


def get_workload_recommendations() -> List[str]:
    """
    Generate actionable workload balancing recommendations.
    
    Returns:
        List of recommendation strings
    
    Raises:
        FileNotFoundError: If team.yaml doesn't exist
    """
    recommendations = []
    
    distribution = analyze_workload_distribution()
    
    # Check if team exists
    if distribution["total_members"] == 0:
        recommendations.append("No team members configured. Run 'stride team init' first.")
        return recommendations
    
    # Check balance score
    balance_score = distribution["balance_score"]
    if balance_score >= 80:
        recommendations.append("✓ Workload is well-balanced across the team.")
    elif balance_score >= 60:
        recommendations.append("⚠ Workload distribution could be improved.")
    else:
        recommendations.append("✗ Workload is significantly imbalanced.")
    
    # Identify overloaded members
    overloaded = identify_overloaded_members()
    if overloaded:
        for member in overloaded:
            recommendations.append(
                f"→ {member['member_name']} has {member['active_count']} sprints "
                f"(load: {member['weighted_load']}) - consider reassigning work"
            )
    
    # Identify underutilized members
    underutilized = identify_underutilized_members()
    if underutilized:
        for member in underutilized:
            recommendations.append(
                f"→ {member['member_name']} has capacity "
                f"({member['active_count']} sprints, load: {member['weighted_load']}) - "
                f"could take on more work"
            )
    
    # Check for unassigned sprints
    all_assignments = get_assigned_sprints(include_unassigned=True)
    unassigned_count = sum(1 for a in all_assignments if a["assignee"] is None)
    if unassigned_count > 0:
        recommendations.append(
            f"→ {unassigned_count} sprint(s) unassigned - run 'stride assign <sprint-id>'"
        )
    
    return recommendations
