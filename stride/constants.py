"""
Project constants and defaults.
"""

from enum import Enum

# Folder names
STRIDE_DIR = ".stride"
SPRINTS_DIR = "sprints"

# File names
PROJECT_FILE = "project.md"
CONFIG_FILE = "config.yaml"

# Sprint Files
FILE_PROPOSAL = "proposal.md"
FILE_PLAN = "plan.md"
FILE_DESIGN = "design.md"
FILE_IMPLEMENTATION = "implementation.md"
FILE_RETROSPECTIVE = "retrospective.md"

class SprintStatus(str, Enum):
    PROPOSED = "proposed"
    ACTIVE = "active"
    REVIEW = "review"
    COMPLETED = "completed"

# Colors for output
COLOR_PROPOSED = "yellow"
COLOR_ACTIVE = "blue"
COLOR_REVIEW = "orange1"
COLOR_COMPLETED = "green"

# Display settings
MAX_TITLE_LENGTH = 50
MAX_TASK_DISPLAY = 10
MAX_LOG_ENTRIES = 5
PROGRESS_BAR_WIDTH = 15
VERBOSE_PROGRESS_BAR_WIDTH = 20

# Markdown patterns (for reference, actual parsing in markdown_parser.py)
CHECKBOX_CHECKED = "[x]"
CHECKBOX_UNCHECKED = "[ ]"

# Learnings Categories
LEARNING_CATEGORIES = [
    "Domain Knowledge",
    "Technical Patterns",
    "Architecture Decisions",
    "Performance Insights",
    "Security Learnings",
    "Testing Strategies"
]

# File Constants
FILE_LEARNINGS = "learnings.md"
FILE_SPEC = "SPEC.md"
FILE_NICE_MANIFEST = "nice_manifest.json"

# NICE Marker Constants
NICE_INTENT_TYPES = [
    "ENTRY", "FLOW", "LOGIC", "TRANSFORM", "IO",
    "STATE", "UI", "INVARIANT", "HOTSPOT",
    "EXPERIMENT", "DEPRECATED"
]

NICE_REQUIRED_TAGS = ["@intent", "@end"]
NICE_RECOMMENDED_TAGS = ["@uid", "@desc", "@inputs", "@outputs", "@agents"]

# Validation Thresholds
TEST_COVERAGE_THRESHOLD = 90
MUTATION_SCORE_THRESHOLD = 80
NICE_COVERAGE_THRESHOLD = 75
