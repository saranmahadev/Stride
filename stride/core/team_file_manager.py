"""
Team file manager for atomic YAML I/O operations.

This module provides safe file operations for team collaboration files:
- .stride/team.yaml
- .stride/sprints/<ID>/.metadata.yaml
- .stride/sprints/<ID>/.comments.yaml

All write operations are atomic (temp file + rename) to prevent corruption.
"""

import yaml
import tempfile
import shutil
from pathlib import Path
from typing import Optional
from datetime import datetime

from ..models import TeamConfig, SprintMetadata, Comment
from ..utils import get_stride_dir


def read_team_config() -> Optional[TeamConfig]:
    """
    Read team configuration from .stride/team.yaml.
    
    Returns:
        TeamConfig object if file exists and is valid, None otherwise.
        
    Raises:
        FileNotFoundError: If .stride/ directory doesn't exist.
        yaml.YAMLError: If team.yaml is malformed.
        ValidationError: If data doesn't match TeamConfig schema.
    """
    stride_dir = get_stride_dir()
    team_file = stride_dir / "team.yaml"
    
    if not team_file.exists():
        return None
    
    with open(team_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    # Convert ISO datetime strings to datetime objects
    if data:
        if 'created_at' in data and isinstance(data['created_at'], str):
            data['created_at'] = datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
        
        for member in data.get('members', []):
            if 'joined_at' in member and isinstance(member['joined_at'], str):
                member['joined_at'] = datetime.fromisoformat(member['joined_at'].replace('Z', '+00:00'))
    
    return TeamConfig(**data) if data else None


def write_team_config(config: TeamConfig) -> None:
    """
    Write team configuration to .stride/team.yaml atomically.
    
    Uses temp file + rename pattern for atomic write.
    
    Args:
        config: TeamConfig object to write.
        
    Raises:
        FileNotFoundError: If .stride/ directory doesn't exist.
        PermissionError: If insufficient permissions to write.
        IOError: If write operation fails.
    """
    stride_dir = get_stride_dir()
    team_file = stride_dir / "team.yaml"
    
    # Convert to dict for YAML serialization
    data = config.model_dump(mode='json')
    
    # Create temp file in same directory for atomic rename
    with tempfile.NamedTemporaryFile(
        mode='w',
        encoding='utf-8',
        dir=stride_dir,
        delete=False,
        suffix='.tmp'
    ) as tmp_file:
        yaml.safe_dump(data, tmp_file, default_flow_style=False, sort_keys=False)
        tmp_path = Path(tmp_file.name)
    
    try:
        # Atomic rename (overwrites existing file)
        shutil.move(str(tmp_path), str(team_file))
    except Exception as e:
        # Clean up temp file if rename fails
        if tmp_path.exists():
            tmp_path.unlink()
        raise IOError(f"Failed to write team.yaml: {e}")


def read_sprint_metadata(sprint_id: str) -> Optional[SprintMetadata]:
    """
    Read sprint metadata from .stride/sprints/<sprint_id>/.metadata.yaml.
    
    Args:
        sprint_id: Sprint identifier (e.g., "sprint-auth").
        
    Returns:
        SprintMetadata object if file exists and is valid, None otherwise.
        
    Raises:
        FileNotFoundError: If sprint directory doesn't exist.
        yaml.YAMLError: If .metadata.yaml is malformed.
        ValidationError: If data doesn't match SprintMetadata schema.
    """
    stride_dir = get_stride_dir()
    sprint_dir = stride_dir / "sprints" / sprint_id
    metadata_file = sprint_dir / ".metadata.yaml"
    
    if not metadata_file.exists():
        return None
    
    with open(metadata_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    # Convert ISO datetime strings to datetime objects
    if data:
        datetime_fields = ['created_at', 'assigned_at']
        for field in datetime_fields:
            if field in data and data[field] and isinstance(data[field], str):
                data[field] = datetime.fromisoformat(data[field].replace('Z', '+00:00'))
        
        # Convert approval timestamps
        for approval in data.get('approvals', []):
            if 'approved_at' in approval and isinstance(approval['approved_at'], str):
                approval['approved_at'] = datetime.fromisoformat(approval['approved_at'].replace('Z', '+00:00'))
        
        # Convert history timestamps
        for event in data.get('history', []):
            if 'timestamp' in event and isinstance(event['timestamp'], str):
                event['timestamp'] = datetime.fromisoformat(event['timestamp'].replace('Z', '+00:00'))
    
    return SprintMetadata(**data) if data else None


def write_sprint_metadata(sprint_id: str, metadata: SprintMetadata) -> None:
    """
    Write sprint metadata to .stride/sprints/<sprint_id>/.metadata.yaml atomically.
    
    Uses temp file + rename pattern for atomic write.
    
    Args:
        sprint_id: Sprint identifier.
        metadata: SprintMetadata object to write.
        
    Raises:
        FileNotFoundError: If sprint directory doesn't exist.
        PermissionError: If insufficient permissions to write.
        IOError: If write operation fails.
    """
    stride_dir = get_stride_dir()
    sprint_dir = stride_dir / "sprints" / sprint_id
    
    if not sprint_dir.exists():
        raise FileNotFoundError(f"Sprint directory not found: {sprint_dir}")
    
    metadata_file = sprint_dir / ".metadata.yaml"
    
    # Convert to dict for YAML serialization
    data = metadata.model_dump(mode='json')
    
    # Create temp file in sprint directory for atomic rename
    with tempfile.NamedTemporaryFile(
        mode='w',
        encoding='utf-8',
        dir=sprint_dir,
        delete=False,
        suffix='.tmp'
    ) as tmp_file:
        yaml.safe_dump(data, tmp_file, default_flow_style=False, sort_keys=False)
        tmp_path = Path(tmp_file.name)
    
    try:
        # Atomic rename
        shutil.move(str(tmp_path), str(metadata_file))
    except Exception as e:
        # Clean up temp file if rename fails
        if tmp_path.exists():
            tmp_path.unlink()
        raise IOError(f"Failed to write .metadata.yaml: {e}")


def read_comments(sprint_id: str) -> list[Comment]:
    """
    Read comments from .stride/sprints/<sprint_id>/.comments.yaml.
    
    Args:
        sprint_id: Sprint identifier.
        
    Returns:
        List of Comment objects. Empty list if file doesn't exist.
        
    Raises:
        FileNotFoundError: If sprint directory doesn't exist.
        yaml.YAMLError: If .comments.yaml is malformed.
        ValidationError: If data doesn't match Comment schema.
    """
    stride_dir = get_stride_dir()
    sprint_dir = stride_dir / "sprints" / sprint_id
    comments_file = sprint_dir / ".comments.yaml"
    
    if not comments_file.exists():
        return []
    
    with open(comments_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    if not data:
        return []
    
    # Recursively convert timestamp strings for nested replies
    def convert_timestamps(comment_data):
        if 'timestamp' in comment_data and isinstance(comment_data['timestamp'], str):
            comment_data['timestamp'] = datetime.fromisoformat(comment_data['timestamp'].replace('Z', '+00:00'))
        
        for reply in comment_data.get('replies', []):
            convert_timestamps(reply)
    
    for comment_data in data:
        convert_timestamps(comment_data)
    
    return [Comment(**comment_data) for comment_data in data]


def append_comment(sprint_id: str, comment: Comment) -> None:
    """
    Append a comment to .stride/sprints/<sprint_id>/.comments.yaml atomically.
    
    Reads existing comments, appends new one, writes atomically.
    
    Args:
        sprint_id: Sprint identifier.
        comment: Comment object to append.
        
    Raises:
        FileNotFoundError: If sprint directory doesn't exist.
        PermissionError: If insufficient permissions to write.
        IOError: If write operation fails.
    """
    stride_dir = get_stride_dir()
    sprint_dir = stride_dir / "sprints" / sprint_id
    
    if not sprint_dir.exists():
        raise FileNotFoundError(f"Sprint directory not found: {sprint_dir}")
    
    comments_file = sprint_dir / ".comments.yaml"
    
    # Read existing comments
    existing_comments = read_comments(sprint_id)
    existing_comments.append(comment)
    
    # Convert to dict for YAML serialization
    data = [c.model_dump(mode='json') for c in existing_comments]
    
    # Create temp file in sprint directory for atomic write
    with tempfile.NamedTemporaryFile(
        mode='w',
        encoding='utf-8',
        dir=sprint_dir,
        delete=False,
        suffix='.tmp'
    ) as tmp_file:
        yaml.safe_dump(data, tmp_file, default_flow_style=False, sort_keys=False)
        tmp_path = Path(tmp_file.name)
    
    try:
        # Atomic rename
        shutil.move(str(tmp_path), str(comments_file))
    except Exception as e:
        # Clean up temp file if rename fails
        if tmp_path.exists():
            tmp_path.unlink()
        raise IOError(f"Failed to write .comments.yaml: {e}")
