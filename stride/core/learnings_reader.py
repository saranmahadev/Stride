import re
from typing import List, Dict, Optional
from pathlib import Path
from stride.models import LearningEntry
from stride.constants import LEARNING_CATEGORIES, FILE_LEARNINGS

# Regex patterns
CATEGORY_REGEX = re.compile(r'^##\s+(.+)$')
SUBCATEGORY_REGEX = re.compile(r'^###\s+(.+)$')
ENTRY_REGEX = re.compile(r'^-\s+\[(\d{4}-\d{2}-\d{2})\]\s+(?:\[(DONE|FAILED)\]\s+)?(?:\((sprint-[^)]+)\):)?\s*(.+)$')
CONTEXT_REGEX = re.compile(r'^\s+\*\*(?:Context|Impact|Solution|Applied in|Applied to):\*\*\s+(.+)$')
CODE_BLOCK_START = re.compile(r'^\s*```(\w+)?')
CODE_BLOCK_END = re.compile(r'^\s*```')

def parse_learnings_file(file_path: Optional[str] = None) -> Dict[str, List[LearningEntry]]:
    """
    Reads Learnings.md and extracts learning entries categorized.
    """
    if not file_path:
        # Default to .stride/Learnings.md
        file_path = str(Path.cwd() / ".stride" / FILE_LEARNINGS)
        
    path = Path(file_path)
    if not path.exists():
        return {cat: [] for cat in LEARNING_CATEGORIES}

    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception:
        return {cat: [] for cat in LEARNING_CATEGORIES}

    learnings = {cat: [] for cat in LEARNING_CATEGORIES}
    
    current_category = None
    current_subcategory = None
    current_entry = None
    in_code_block = False
    code_lines = []
    
    for line in lines:
        line_stripped = line.strip()
        
        # Handle Code Blocks
        if in_code_block:
            if CODE_BLOCK_END.match(line_stripped):
                in_code_block = False
                if current_entry:
                    current_entry.pattern_code = "\n".join(code_lines)
                code_lines = []
            else:
                code_lines.append(line.rstrip())
            continue
            
        if CODE_BLOCK_START.match(line_stripped):
            in_code_block = True
            continue

        # Parse Categories
        cat_match = CATEGORY_REGEX.match(line_stripped)
        if cat_match:
            cat_name = cat_match.group(1).strip()
            # Normalize category name to match constants if possible
            for known_cat in LEARNING_CATEGORIES:
                if known_cat.lower() == cat_name.lower():
                    current_category = known_cat
                    break
            else:
                current_category = cat_name
            current_subcategory = None
            continue

        # Parse Subcategories
        sub_match = SUBCATEGORY_REGEX.match(line_stripped)
        if sub_match:
            current_subcategory = sub_match.group(1).strip()
            continue

        # Parse Entries
        entry_match = ENTRY_REGEX.match(line_stripped)
        if entry_match:
            if current_category:
                date_str = entry_match.group(1)
                status = entry_match.group(2) # DONE or FAILED
                sprint_id = entry_match.group(3) or "unknown"
                content = entry_match.group(4)
                
                is_antipattern = (status == "FAILED")
                
                current_entry = LearningEntry(
                    category=current_category,
                    subcategory=current_subcategory or "General",
                    content=content,
                    context="",
                    sprint_id=sprint_id,
                    is_antipattern=is_antipattern,
                    timestamp=date_str,
                    pattern_code=None
                )
                
                if current_category in learnings:
                    learnings[current_category].append(current_entry)
                else:
                    # Handle unknown categories
                    if "Uncategorized" not in learnings:
                        learnings["Uncategorized"] = []
                    learnings["Uncategorized"].append(current_entry)
            continue

        # Parse Context/Metadata
        context_match = CONTEXT_REGEX.match(line_stripped)
        if context_match and current_entry:
            context_text = context_match.group(1)
            if current_entry.context:
                current_entry.context += f"; {context_text}"
            else:
                current_entry.context = context_text
            continue

    return learnings

def search_learnings(query: str, category: Optional[str] = None, is_antipattern: Optional[bool] = None) -> List[LearningEntry]:
    """
    Searches across all learnings.
    """
    all_learnings = parse_learnings_file()
    results = []
    
    query_lower = query.lower()
    
    for cat, entries in all_learnings.items():
        if category and cat.lower() != category.lower():
            continue
            
        for entry in entries:
            if is_antipattern is not None and entry.is_antipattern != is_antipattern:
                continue
                
            # Search in content, context, subcategory
            if (query_lower in entry.content.lower() or 
                query_lower in entry.context.lower() or 
                query_lower in entry.subcategory.lower()):
                results.append(entry)
                
    return results

def get_category_learnings(category: str, subcategory: Optional[str] = None) -> List[LearningEntry]:
    """
    Returns all learnings in specific category.
    """
    all_learnings = parse_learnings_file()
    
    # Find matching category key
    target_cat = None
    for cat in all_learnings.keys():
        if cat.lower() == category.lower():
            target_cat = cat
            break
            
    if not target_cat:
        return []
        
    entries = all_learnings[target_cat]
    
    if subcategory:
        return [e for e in entries if e.subcategory.lower() == subcategory.lower()]
        
    return entries

def get_antipatterns() -> List[LearningEntry]:
    """
    Returns all anti-patterns across categories.
    """
    all_learnings = parse_learnings_file()
    antipatterns = []
    
    for entries in all_learnings.values():
        antipatterns.extend([e for e in entries if e.is_antipattern])
        
    return antipatterns
