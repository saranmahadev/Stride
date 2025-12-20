import os
import re
import hashlib
from typing import List, Dict, Any, Tuple, Optional
from pathlib import Path
from stride.models import NiceBlock

# Regex patterns for parsing
INTENT_START_REGEX = re.compile(r'^\s*(?:#|//|/\*|<!--)\s*@intent\s+(\w+)\s+(\w+)')
TAG_REGEX = re.compile(r'^\s*(?:#|//|\*)\s*@(\w+)\s*(.*)')
END_REGEX = re.compile(r'^\s*(?:#|//|\*|-->)\s*@end')

def parse_file(file_path: str) -> List[NiceBlock]:
    """
    Reads source file and extracts intent blocks.
    """
    blocks = []
    path = Path(file_path)
    
    if not path.exists():
        return []

    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except (UnicodeDecodeError, PermissionError, OSError):
        return [] # Skip binary or unreadable files

    i = 0
    while i < len(lines):
        line = lines[i]
        match = INTENT_START_REGEX.match(line)
        if match:
            block, end_line = extract_intent_block(lines, i, str(path))
            if block:
                blocks.append(block)
                i = end_line
            else:
                i += 1
        else:
            i += 1
            
    return blocks

def parse_directory(dir_path: str, recursive: bool = True) -> List[NiceBlock]:
    """
    Scans directory for all source files and extracts markers.
    """
    all_blocks = []
    path = Path(dir_path)
    
    if not path.exists():
        return []

    # Skip hidden directories and common ignore patterns
    skip_dirs = {'.git', '__pycache__', 'node_modules', '.stride', 'site', 'venv', 'env'}
    
    for root, dirs, files in os.walk(path):
        # Modify dirs in-place to skip ignored directories
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        if not recursive and root != str(path):
            continue
            
        for file in files:
            if file.startswith('.'):
                continue
                
            file_path = os.path.join(root, file)
            # Try to parse every file, parse_file handles unreadable ones
            all_blocks.extend(parse_file(file_path))
                
    return all_blocks

def extract_intent_block(lines: List[str], start_line: int, file_path: str) -> Tuple[Optional[NiceBlock], int]:
    """
    Parses single intent block from line array.
    Returns (NiceBlock, end_line_index).
    """
    # Parse the start line
    start_match = INTENT_START_REGEX.match(lines[start_line])
    if not start_match:
        return None, start_line

    intent_type = start_match.group(1)
    intent_id = start_match.group(2)
    
    tags = {}
    current_line = start_line + 1
    content_lines = [lines[start_line]]
    
    while current_line < len(lines):
        line = lines[current_line]
        content_lines.append(line)
        
        # Check for end tag
        if END_REGEX.match(line):
            break
            
        # Parse other tags
        tag_match = TAG_REGEX.match(line)
        if tag_match:
            tag_name = tag_match.group(1)
            tag_value = tag_match.group(2).strip()
            
            # Handle list-like tags
            if tag_name in ['inputs', 'outputs', 'fail', 'forbid', 'suggestions', 'errors', 'warnings']:
                # Simple comma separation for now, could be more robust
                tags[tag_name] = [x.strip() for x in tag_value.split(',') if x.strip()]
            elif tag_name == 'depends':
                # Parse dependency format: [strength:]<uid>
                if 'depends' not in tags:
                    tags['depends'] = []
                tags['depends'].append(tag_value)
            else:
                tags[tag_name] = tag_value
        
        current_line += 1
        
    # If we reached end of file without @end, it's not a valid block
    if current_line >= len(lines):
        return None, current_line

    # Calculate semantic hash
    semantic_content = "".join(content_lines)
    semantic_hash = hashlib.md5(semantic_content.encode('utf-8')).hexdigest()
    
    # Extract UID if present, otherwise construct a temporary one or leave empty
    uid = tags.get('uid', f"nice:{intent_type.lower()}:unknown:{intent_id}:v1")
    
    block = NiceBlock(
        intent_type=intent_type,
        id=intent_id,
        uid=uid,
        file_path=file_path,
        line_range=(start_line + 1, current_line + 1), # 1-based indexing
        tags=tags,
        semantic_hash=semantic_hash
    )
    
    return block, current_line

def build_dependency_graph(blocks: List[NiceBlock]) -> Dict[str, List[str]]:
    """
    Extracts @depends tags from all blocks and creates adjacency list.
    Returns Dict[uid, List[dependency_uids]]
    """
    graph = {}
    
    # Initialize all nodes
    for block in blocks:
        graph[block.uid] = []
        
    # Add edges
    for block in blocks:
        if 'depends' in block.tags:
            deps = block.tags['depends']
            if isinstance(deps, list):
                for dep in deps:
                    # Handle "strength:uid" format
                    if ':' in dep and not dep.startswith('nice:'):
                        parts = dep.split(':', 1)
                        if len(parts) == 2 and parts[1].startswith('nice:'):
                            dep_uid = parts[1]
                        else:
                            dep_uid = dep
                    else:
                        dep_uid = dep
                    
                    graph[block.uid].append(dep_uid.strip())
            elif isinstance(deps, str):
                 # Handle single dependency string case if parser didn't split it
                 # (Though extract_intent_block handles 'depends' as list append)
                 pass

    return graph
