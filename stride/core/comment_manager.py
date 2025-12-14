"""
Comment and communication management for sprints.

This module provides functions for adding, retrieving, and managing
threaded comments on sprints with optional file/line anchoring.
"""

from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime

from stride.models import Comment
from stride.core.team_file_manager import read_comments, append_comment, read_team_config
from stride.utils import get_stride_dir


def add_comment(
    sprint_id: str,
    author_email: str,
    content: str,
    file_path: Optional[str] = None,
    line_number: Optional[int] = None,
    parent_id: Optional[str] = None
) -> Comment:
    """
    Add a comment to a sprint.
    
    Args:
        sprint_id: Sprint identifier
        author_email: Email of comment author
        content: Comment text (markdown supported)
        file_path: Optional file path being commented on
        line_number: Optional line number in file
        parent_id: Optional parent comment ID for replies
    
    Returns:
        Created Comment object
    
    Raises:
        FileNotFoundError: If sprint directory doesn't exist
        ValueError: If author not in team.yaml
    """
    # Validate author
    try:
        team_config = read_team_config()
        author = team_config.get_member(author_email)
        if not author:
            raise ValueError(f"Author '{author_email}' not found in team.yaml")
    except FileNotFoundError:
        # No team config, allow any author
        pass
    
    # Check sprint exists
    stride_dir = get_stride_dir()
    sprint_dir = stride_dir / "sprints" / sprint_id
    if not sprint_dir.exists():
        raise FileNotFoundError(f"Sprint directory not found: {sprint_dir}")
    
    # Create comment
    comment = Comment(
        id=f"c{int(datetime.now().timestamp() * 1000)}",  # Millisecond timestamp
        author=author_email,
        content=content,
        created_at=datetime.now(),
        file_path=file_path,
        line_number=line_number,
        replies=[]
    )
    
    # Append to comments file
    append_comment(sprint_id, comment, parent_id=parent_id)
    
    return comment


def get_comments(
    sprint_id: str,
    file_path: Optional[str] = None,
    unresolved_only: bool = False,
    flat: bool = False
) -> List[Comment]:
    """
    Get comments for a sprint.
    
    Args:
        sprint_id: Sprint identifier
        file_path: Filter by file path (None returns all)
        unresolved_only: Only return unresolved comments
        flat: Flatten nested replies into single list
    
    Returns:
        List of Comment objects (threaded unless flat=True)
    
    Raises:
        FileNotFoundError: If sprint directory doesn't exist
    """
    # Check sprint exists
    stride_dir = get_stride_dir()
    sprint_dir = stride_dir / "sprints" / sprint_id
    if not sprint_dir.exists():
        raise FileNotFoundError(f"Sprint directory not found: {sprint_dir}")
    
    # Read comments
    comments = read_comments(sprint_id)
    
    # Filter by file path
    if file_path:
        comments = [c for c in comments if c.file_path == file_path]
    
    # Filter by resolved status
    if unresolved_only:
        comments = [c for c in comments if not c.is_resolved]
    
    # Flatten if requested
    if flat:
        comments = _flatten_comments(comments)
    
    return comments


def _flatten_comments(comments: List[Comment]) -> List[Comment]:
    """Recursively flatten comment tree into list."""
    flat = []
    for comment in comments:
        flat.append(comment)
        if comment.replies:
            flat.extend(_flatten_comments(comment.replies))
    return flat


def resolve_comment(
    sprint_id: str,
    comment_id: str,
    resolver_email: str
) -> Comment:
    """
    Mark a comment as resolved.
    
    Args:
        sprint_id: Sprint identifier
        comment_id: Comment ID to resolve
        resolver_email: Email of person resolving
    
    Returns:
        Updated Comment object
    
    Raises:
        FileNotFoundError: If sprint directory doesn't exist
        ValueError: If comment not found
    """
    # Check sprint exists
    stride_dir = get_stride_dir()
    sprint_dir = stride_dir / "sprints" / sprint_id
    if not sprint_dir.exists():
        raise FileNotFoundError(f"Sprint directory not found: {sprint_dir}")
    
    # Read all comments
    comments = read_comments(sprint_id)
    
    # Find and update comment
    comment = _find_comment_by_id(comments, comment_id)
    if not comment:
        raise ValueError(f"Comment '{comment_id}' not found in sprint {sprint_id}")
    
    # Mark as resolved
    comment.resolved = True
    comment.resolved_by = resolver_email
    comment.resolved_at = datetime.now()
    
    # Write back comments
    from stride.core.team_file_manager import write_comments
    _write_comments_helper(sprint_id, comments)
    
    return comment


def unresolve_comment(
    sprint_id: str,
    comment_id: str
) -> Comment:
    """
    Mark a resolved comment as unresolved.
    
    Args:
        sprint_id: Sprint identifier
        comment_id: Comment ID to unresolve
    
    Returns:
        Updated Comment object
    
    Raises:
        FileNotFoundError: If sprint directory doesn't exist
        ValueError: If comment not found
    """
    # Check sprint exists
    stride_dir = get_stride_dir()
    sprint_dir = stride_dir / "sprints" / sprint_id
    if not sprint_dir.exists():
        raise FileNotFoundError(f"Sprint directory not found: {sprint_dir}")
    
    # Read all comments
    comments = read_comments(sprint_id)
    
    # Find and update comment
    comment = _find_comment_by_id(comments, comment_id)
    if not comment:
        raise ValueError(f"Comment '{comment_id}' not found")
    
    # Mark as unresolved
    comment.resolved = False
    comment.resolved_by = None
    comment.resolved_at = None
    
    # Write back comments
    _write_comments_helper(sprint_id, comments)
    
    return comment


def reply_to_comment(
    sprint_id: str,
    parent_id: str,
    author_email: str,
    content: str
) -> Comment:
    """
    Add a reply to an existing comment.
    
    Args:
        sprint_id: Sprint identifier
        parent_id: Parent comment ID
        author_email: Email of reply author
        content: Reply text
    
    Returns:
        Created Comment object (the reply)
    
    Raises:
        FileNotFoundError: If sprint directory doesn't exist
        ValueError: If parent comment not found
    """
    # Validate author
    try:
        team_config = read_team_config()
        author = team_config.get_member(author_email)
        if not author:
            raise ValueError(f"Author '{author_email}' not found in team.yaml")
    except FileNotFoundError:
        # No team config, allow any author
        pass
    
    # Check sprint exists
    stride_dir = get_stride_dir()
    sprint_dir = stride_dir / "sprints" / sprint_id
    if not sprint_dir.exists():
        raise FileNotFoundError(f"Sprint directory not found: {sprint_dir}")
    
    # Read comments to verify parent exists
    comments = read_comments(sprint_id)
    parent = _find_comment_by_id(comments, parent_id)
    if not parent:
        raise ValueError(f"Parent comment '{parent_id}' not found")
    
    # Create reply
    reply = Comment(
        id=f"c{int(datetime.now().timestamp() * 1000)}",
        author=author_email,
        content=content,
        created_at=datetime.now(),
        file_path=parent.file_path,  # Inherit from parent
        line_number=parent.line_number,  # Inherit from parent
        replies=[]
    )
    
    # Append using team_file_manager
    append_comment(sprint_id, reply, parent_id=parent_id)
    
    return reply


def _find_comment_by_id(comments: List[Comment], comment_id: str) -> Optional[Comment]:
    """Recursively find comment by ID in tree."""
    for comment in comments:
        if comment.id == comment_id:
            return comment
        if comment.replies:
            found = _find_comment_by_id(comment.replies, comment_id)
            if found:
                return found
    return None


def _write_comments_helper(sprint_id: str, comments: List[Comment]):
    """Write comments to file (wrapper for atomic write)."""
    import yaml
    import tempfile
    import shutil
    
    stride_dir = get_stride_dir()
    comments_file = stride_dir / "sprints" / sprint_id / ".comments.yaml"
    
    # Convert to dict for YAML
    def comment_to_dict(c: Comment) -> dict:
        data = {
            "id": c.id,
            "author": c.author,
            "content": c.content,
            "created_at": c.created_at.isoformat(),
            "resolved": c.resolved
        }
        if c.file_path:
            data["file_path"] = c.file_path
        if c.line_number:
            data["line_number"] = c.line_number
        if c.resolved_by:
            data["resolved_by"] = c.resolved_by
        if c.resolved_at:
            data["resolved_at"] = c.resolved_at.isoformat()
        if c.replies:
            data["replies"] = [comment_to_dict(r) for r in c.replies]
        return data
    
    data = [comment_to_dict(c) for c in comments]
    
    # Atomic write
    with tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.yaml',
        dir=comments_file.parent,
        delete=False
    ) as tmp:
        yaml.safe_dump(data, tmp, default_flow_style=False, sort_keys=False)
        tmp_path = tmp.name
    
    shutil.move(tmp_path, comments_file)


def get_comment_stats(sprint_id: str) -> Dict[str, any]:
    """
    Get comment statistics for a sprint.
    
    Args:
        sprint_id: Sprint identifier
    
    Returns:
        Dict with total, unresolved, resolved, files_with_comments
    
    Raises:
        FileNotFoundError: If sprint directory doesn't exist
    """
    # Check sprint exists
    stride_dir = get_stride_dir()
    sprint_dir = stride_dir / "sprints" / sprint_id
    if not sprint_dir.exists():
        raise FileNotFoundError(f"Sprint directory not found: {sprint_dir}")
    
    # Read comments
    comments = read_comments(sprint_id)
    flat_comments = _flatten_comments(comments)
    
    # Calculate stats
    total = len(flat_comments)
    unresolved = sum(1 for c in flat_comments if not c.is_resolved)
    resolved = sum(1 for c in flat_comments if c.is_resolved)
    
    # Get unique files
    files_with_comments = set()
    for c in flat_comments:
        if c.file_path:
            files_with_comments.add(c.file_path)
    
    return {
        "total": total,
        "unresolved": unresolved,
        "resolved": resolved,
        "files_with_comments": list(files_with_comments)
    }
